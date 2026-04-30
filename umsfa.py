"""
Universal MS Format Archiver (UMSFA)
Архиватор с поддержкой AES-256 шифрования
"""

import os
import tarfile
import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import secrets
from tqdm import tqdm


CHUNK_SIZE = 1024 * 1024


class ProgressReader:
    def __init__(self, fileobj, progress_bar, total_bytes, update_callback):
        self.fileobj = fileobj
        self.progress_bar = progress_bar
        self.total_bytes = total_bytes
        self.update_callback = update_callback

    def read(self, size=-1):
        chunk = self.fileobj.read(size)
        if chunk:
            self.progress_bar.update(len(chunk))
            self.update_callback(self.progress_bar, int(self.progress_bar.n), self.total_bytes)
        return chunk


class MSArchiver:
    """Архиватор в формат .ms с AES-256 шифрованием"""
    
    MAGIC = b'UMSFA1.0'  # Сигнатура формата
    SALT_SIZE = 16
    IV_SIZE = 16
    KEY_SIZE = 32  # 256 бит для AES-256
    ITERATIONS = 100000
    
    def __init__(
        self,
        password: str = None,
        use_compression: bool = False,
        compression_level: int = 6
    ):
        """
        Инициализация архиватора
        
        Args:
            password: Пароль для шифрования (если None - без шифрования)
            use_compression: Использовать gzip-сжатие при создании архива
            compression_level: Уровень gzip-сжатия от 1 до 9
        """
        self.password = password
        self.use_compression = use_compression
        self.compression_level = compression_level
        self.backend = default_backend()
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Получение ключа из пароля через PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=self.ITERATIONS,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def _encrypt_data(self, data: bytes, password: str) -> tuple:
        """
        Шифрование данных AES-256-CBC
        
        Returns:
            (encrypted_data, salt, iv)
        """
        salt = secrets.token_bytes(self.SALT_SIZE)
        iv = secrets.token_bytes(self.IV_SIZE)
        key = self._derive_key(password, salt)
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Добавление PKCS7 padding
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length] * padding_length)
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_data, salt, iv
    
    def _decrypt_data(self, encrypted_data: bytes, password: str, salt: bytes, iv: bytes) -> bytes:
        """Расшифровка данных AES-256-CBC"""
        key = self._derive_key(password, salt)
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Удаление PKCS7 padding
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]

    @staticmethod
    def _format_size(size: int) -> str:
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        value = float(size)
        for unit in units:
            if value < 1024 or unit == units[-1]:
                if unit == 'B':
                    return f"{int(value)} {unit}"
                return f"{value:.2f} {unit}"
            value /= 1024

    def _make_progress_bar(self, description: str, total_bytes: int):
        progress_total = max(total_bytes, 1)
        progress_bar = tqdm(
            total=progress_total,
            desc=description,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            leave=True,
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}'
        )
        self._update_progress_bar(progress_bar, 0, total_bytes)
        return progress_bar

    def _update_progress_bar(self, progress_bar, processed_bytes: int, total_bytes: int):
        remaining_bytes = max(total_bytes - processed_bytes, 0)
        progress_bar.set_postfix_str(
            f"обработано {self._format_size(processed_bytes)}, осталось {self._format_size(remaining_bytes)}"
        )

    def _collect_source_entries(self, source: Path):
        source = source.resolve()
        root_name = source.name or source.anchor.rstrip('\\/') or 'root'
        entries = [(source, Path(root_name))]

        if source.is_dir():
            for child in sorted(source.rglob('*')):
                relative_path = child.relative_to(source)
                entries.append((child, Path(root_name) / relative_path))

        total_bytes = sum(path.stat().st_size for path, _ in entries if path.is_file())
        return entries, total_bytes, root_name

    def _add_entry_to_tar(self, tar: tarfile.TarFile, source_path: Path, arcname: Path, progress_bar, total_bytes: int):
        tarinfo = tar.gettarinfo(str(source_path), arcname=str(arcname))

        if tarinfo.isreg():
            with open(source_path, 'rb') as source_file:
                wrapped_file = ProgressReader(source_file, progress_bar, total_bytes, self._update_progress_bar)
                tar.addfile(tarinfo, fileobj=wrapped_file)
            return

        tar.addfile(tarinfo)

    def _validate_tar_member(self, output_path: Path, member: tarfile.TarInfo):
        destination = (output_path / member.name).resolve()
        if not self._is_within_directory(output_path, destination):
            raise ValueError(f"Обнаружен небезопасный путь в архиве: {member.name}")

    def _extract_member(self, tar: tarfile.TarFile, member: tarfile.TarInfo, output_path: Path, progress_bar, total_bytes: int):
        self._validate_tar_member(output_path, member)
        destination = output_path / member.name

        if member.isdir():
            destination.mkdir(parents=True, exist_ok=True)
            return

        if member.isreg():
            destination.parent.mkdir(parents=True, exist_ok=True)
            extracted_file = tar.extractfile(member)
            if extracted_file is None:
                raise ValueError(f"Не удалось прочитать содержимое файла: {member.name}")

            with extracted_file, open(destination, 'wb') as target_file:
                while True:
                    chunk = extracted_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    target_file.write(chunk)
                    progress_bar.update(len(chunk))
                    self._update_progress_bar(progress_bar, int(progress_bar.n), total_bytes)

            self._apply_member_metadata(destination, member)
            return

        tar.extract(member, path=output_path)

    @staticmethod
    def _apply_member_metadata(destination: Path, member: tarfile.TarInfo):
        try:
            os.chmod(destination, member.mode)
        except OSError:
            pass

        try:
            os.utime(destination, (member.mtime, member.mtime))
        except OSError:
            pass

    @staticmethod
    def _is_within_directory(directory: Path, target: Path) -> bool:
        try:
            target.resolve().relative_to(directory.resolve())
            return True
        except ValueError:
            return False
    
    def archive(self, source_path: str, output_path: str, progress_callback=None) -> bool:
        """
        Архивирование папки/файла в .ms формат
        
        Args:
            source_path: Путь к файлу/папке
            output_path: Путь к выходному .ms файлу
            progress_callback: Функция обратного вызова для прогресса
        
        Returns:
            True если успешно, False иначе
        """
        try:
            source = Path(source_path)
            if not source.exists():
                print(f"Ошибка: {source_path} не существует.")
                return False
            source_display_name = source.resolve().name or source.name or 'root'
            entries, total_bytes, _ = self._collect_source_entries(source)
            
            # Создание временного tar файла
            temp_tar = output_path + '.tmp'
            tar_mode = 'w:gz' if self.use_compression else 'w'
            
            print(f"Архивирование {source_path}...")
            with self._make_progress_bar("Архивация", total_bytes) as progress_bar:
                tar_kwargs = {}
                if self.use_compression:
                    tar_kwargs['compresslevel'] = self.compression_level

                with tarfile.open(temp_tar, tar_mode, **tar_kwargs) as tar:
                    for entry_path, arcname in entries:
                        self._add_entry_to_tar(tar, entry_path, arcname, progress_bar, total_bytes)
            
            # Чтение архива в памяти
            with open(temp_tar, 'rb') as f:
                tar_data = f.read()
            
            os.remove(temp_tar)
            
            # Создание метаданных
            metadata = {
                'source_name': source_display_name,
                'source_type': 'directory' if source.is_dir() else 'file',
                'original_size': len(tar_data),
                'encrypted': bool(self.password),
                'compressed': self.use_compression,
                'compression_method': 'gzip' if self.use_compression else 'none',
                'compression_level': self.compression_level if self.use_compression else 0,
            }
            
            print("Шифрование (AES-256)...")
            
            if self.password:
                encrypted_data, salt, iv = self._encrypt_data(tar_data, self.password)
                metadata['salt'] = salt.hex()
                metadata['iv'] = iv.hex()
            else:
                encrypted_data = tar_data
                metadata['salt'] = ''
                metadata['iv'] = ''
            
            # Запись .ms файла
            with open(output_path, 'wb') as f:
                f.write(self.MAGIC)
                
                # Запись размера метаданных (4 байта)
                metadata_json = json.dumps(metadata).encode()
                f.write(len(metadata_json).to_bytes(4, byteorder='big'))
                
                # Запись метаданных
                f.write(metadata_json)
                
                # Запись шифрованных данных
                f.write(encrypted_data)
            
            file_size = os.path.getsize(output_path)
            print(f"Архив создан: {output_path}")
            print(f"   Размер: {file_size / 1024 / 1024:.2f} МБ")
            
            return True
            
        except Exception as e:
            print(f"Ошибка при архивировании: {e}")
            return False
    
    def extract(self, archive_path: str, output_dir: str, progress_callback=None) -> bool:
        """
        Разархивирование .ms файла
        
        Args:
            archive_path: Путь к .ms архиву
            output_dir: Директория для распаковки
            progress_callback: Функция обратного вызова для прогресса
        
        Returns:
            True если успешно, False иначе
        """
        try:
            archive = Path(archive_path)
            if not archive.exists():
                print(f"Ошибка: {archive_path} не найден.")
                return False
            
            print(f"Чтение архива {archive_path}...")
            
            with open(archive, 'rb') as f:
                # Проверка сигнатуры
                magic = f.read(len(self.MAGIC))
                if magic != self.MAGIC:
                    print("Ошибка: некорректный формат файла.")
                    return False
                
                # Чтение размера метаданных
                metadata_size = int.from_bytes(f.read(4), byteorder='big')
                
                # Чтение метаданных
                metadata_json = f.read(metadata_size).decode()
                metadata = json.loads(metadata_json)
                
                # Чтение шифрованных данных
                encrypted_data = f.read()

            is_compressed = metadata.get('compressed')
            if is_compressed is None:
                is_compressed = True
            
            # Расшифровка
            if metadata['encrypted']:
                if not self.password:
                    print("Ошибка: архив зашифрован, введите пароль.")
                    return False
                
                print("Расшифровка (AES-256)...")
                salt = bytes.fromhex(metadata['salt'])
                iv = bytes.fromhex(metadata['iv'])
                
                try:
                    tar_data = self._decrypt_data(encrypted_data, self.password, salt, iv)
                except Exception as e:
                    print("Ошибка: неверный пароль или повреждённые данные.")
                    return False
            else:
                tar_data = encrypted_data
            
            # Распаковка tar архива
            temp_tar = archive_path + '.tmp'
            with open(temp_tar, 'wb') as f:
                f.write(tar_data)
            
            print("Распаковка...")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            tar_mode = 'r:gz' if is_compressed else 'r:'
            with tarfile.open(temp_tar, tar_mode) as tar:
                members = tar.getmembers()
                total_bytes = sum(member.size for member in members if member.isreg())

                with self._make_progress_bar("Распаковка", total_bytes) as progress_bar:
                    for member in members:
                        self._extract_member(tar, member, output_path, progress_bar, total_bytes)
            
            os.remove(temp_tar)
            
            print(f"Архив распакован в: {output_dir}")
            print(f"   Исходный размер: {metadata['original_size'] / 1024 / 1024:.2f} МБ")
            
            return True
            
        except Exception as e:
            print(f"Ошибка при распаковке: {e}")
            return False
    
    def get_archive_info(self, archive_path: str) -> dict:
        """Получение информации об архиве"""
        try:
            with open(archive_path, 'rb') as f:
                magic = f.read(len(self.MAGIC))
                if magic != self.MAGIC:
                    return None
                
                metadata_size = int.from_bytes(f.read(4), byteorder='big')
                metadata_json = f.read(metadata_size).decode()
                metadata = json.loads(metadata_json)
                
                return metadata
        except:
            return None
