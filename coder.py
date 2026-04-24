import cv2
import numpy as np
import os
import math
import subprocess
import tempfile
import shutil
import sys
import re
import hashlib
from pathlib import Path
from typing import Optional

class YouTubeEncoder:
    def __init__(self, key: Optional[str] = None):
        self.width = 1920
        self.height = 1080
        self.fps = 6
        self.max_file_size = 100 * 1024 * 1024
        
        self.block_height = 16
        self.block_width = 24
        self.spacing = 4
        
        if key and key.strip():
            self.key = hashlib.sha256(key.encode()).digest()
            self.use_encryption = True
        else:
            self.key = None
            self.use_encryption = False
        
        self.colors = {
            '0000': (255, 0, 0),
            '0001': (0, 255, 0),
            '0010': (0, 0, 255),
            '0011': (255, 255, 0),
            '0100': (255, 0, 255),
            '0101': (0, 255, 255),
            '0110': (255, 128, 0),
            '0111': (128, 0, 255),
            '1000': (0, 128, 128),
            '1001': (128, 128, 0),
            '1010': (128, 0, 128),
            '1011': (0, 128, 0),
            '1100': (128, 0, 0),
            '1101': (0, 0, 128),
            '1110': (192, 192, 192),
            '1111': (255, 255, 255)
        }
        
        self.marker_size = 80
        self.blocks_x = (self.width - 2*self.marker_size) // (self.block_width + self.spacing)
        self.blocks_y = (self.height - 2*self.marker_size) // (self.block_height + self.spacing)
        self.blocks_per_region = self.blocks_x * self.blocks_y
        self.blocks_per_frame = self.blocks_per_region * 3
        
        self.eof_marker = "█" * 64
        self.eof_bytes = self.eof_marker.encode('utf-8')
    
    def _sanitize_filename(self, filename: str) -> str:
        name = Path(filename).name
        name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
        parts = name.rsplit('.', 1)
        if len(parts) > 1:
            dangerous = {'.exe', '.bat', '.sh', '.py', '.js', '.dll', '.so', '.com'}
            if f".{parts[1].lower()}" in dangerous:
                name = f"{parts[0]}.bin"
        return name or "file.bin"
    
    def _validate_input_file(self, filepath: str) -> Path:
        path = Path(filepath).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        if not path.is_file():
            raise ValueError(f"Не является файлом: {filepath}")
        if path.stat().st_size > self.max_file_size:
            raise ValueError(f"Файл слишком большой: {path.stat().st_size} байт")
        if path.stat().st_size == 0:
            raise ValueError("Файл пуст")
        return path
    
    def _encrypt_data(self, data: bytes) -> bytes:
        if not self.use_encryption:
            return data
        
        result = bytearray()
        key_len = len(self.key)
        for i, byte in enumerate(data):
            result.append(byte ^ self.key[i % key_len])
        return bytes(result)
    
    def _draw_markers(self, frame: np.ndarray) -> np.ndarray:
        for x, y in [(0, 0), (self.width-self.marker_size, 0),
                     (0, self.height-self.marker_size),
                     (self.width-self.marker_size, self.height-self.marker_size)]:
            cv2.rectangle(frame, (x, y), (x+self.marker_size, y+self.marker_size),
                         (255, 255, 255), -1)
            cv2.rectangle(frame, (x, y), (x+self.marker_size, y+self.marker_size),
                         (0, 0, 0), 2)
        return frame
    
    def _draw_block(self, frame: np.ndarray, x: int, y: int, color: tuple) -> bool:
        x1 = self.marker_size + x * (self.block_width + self.spacing)
        y1 = self.marker_size + y * (self.block_height + self.spacing)
        x2 = x1 + self.block_width
        y2 = y1 + self.block_height
        
        if x2 > self.width - self.marker_size or y2 > self.height - self.marker_size:
            return False
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 1)
        return True
    
    def _bits_to_color(self, bits: str) -> tuple:
        while len(bits) < 4:
            bits = '0' + bits
        return self.colors.get(bits, (255, 0, 0))
    
    def _data_to_blocks(self, data: bytes) -> list:
        all_bits = []
        for byte in data:
            for i in range(7, -1, -1):
                all_bits.append(str((byte >> i) & 1))
        
        while len(all_bits) % 4 != 0:
            all_bits.append('0')
        
        return [''.join(all_bits[i:i+4]) for i in range(0, len(all_bits), 4)]
    
    def encode(self, input_file: str, output_file: str = "output.mp4") -> bool:
        try:
            input_path = self._validate_input_file(input_file)
        except (FileNotFoundError, ValueError) as e:
            print(f"❌ {e}")
            return False
        
        output_path = Path(output_file).resolve()
        if not output_path.suffix or output_path.suffix.lower() != '.mp4':
            output_path = output_path.with_suffix('.mp4')
        
        original_filename = self._sanitize_filename(input_path.name)
        
        print(f"📤 Кодирование: {original_filename}")
        print(f"📦 Размер: {input_path.stat().st_size} байт")
        
        try:
            with open(input_path, 'rb') as f:
                data = f.read()
        except IOError as e:
            print(f"❌ Ошибка чтения файла: {e}")
            return False
        
        if self.use_encryption:
            encrypted_data = self._encrypt_data(data)
            print("🔐 Данные зашифрованы")
        else:
            encrypted_data = data
        
        header = f"FILE:{original_filename}:SIZE:{len(data)}|"
        try:
            header_bytes = header.encode('latin-1')
        except UnicodeEncodeError:
            print("❌ Недопустимые символы в имени файла")
            return False
        
        header_blocks = self._data_to_blocks(header_bytes)
        data_blocks = self._data_to_blocks(encrypted_data)
        eof_blocks = self._data_to_blocks(self.eof_bytes)
        all_blocks = header_blocks + data_blocks + eof_blocks
        
        frames_needed = math.ceil(len(all_blocks) / self.blocks_per_frame) + 5
        
        temp_dir = tempfile.mkdtemp(prefix="youtube_encoder_")
        print(f"🎬 Кадров: {frames_needed} ({frames_needed/self.fps:.1f} сек)")
        
        try:
            for frame_num in range(frames_needed - 5):
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                frame = self._draw_markers(frame)
                
                start_idx = frame_num * self.blocks_per_frame
                end_idx = min(start_idx + self.blocks_per_frame, len(all_blocks))
                frame_blocks = all_blocks[start_idx:end_idx]
                
                for region in range(3):
                    offset_y = (region % 2) * self.blocks_y
                    offset_x = (region // 2) * self.blocks_x
                    
                    for idx, bits in enumerate(frame_blocks):
                        y = offset_y + idx // self.blocks_x
                        x = offset_x + idx % self.blocks_x
                        if y < self.blocks_y * 2 and x < self.blocks_x * 2:
                            color = self._bits_to_color(bits)
                            self._draw_block(frame, x, y, color)
                
                frame_file = os.path.join(temp_dir, f"frame_{frame_num:05d}.png")
                cv2.imwrite(frame_file, frame)
            
            for i in range(5):
                frame_num = frames_needed - 5 + i
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                frame = self._draw_markers(frame)
                for y in range(self.blocks_y * 2):
                    for x in range(self.blocks_x * 2):
                        self._draw_block(frame, x, y, (255, 0, 0))
                frame_file = os.path.join(temp_dir, f"frame_{frame_num:05d}.png")
                cv2.imwrite(frame_file, frame)
            
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                
                cmd = [
                    'ffmpeg', '-framerate', str(self.fps),
                    '-i', os.path.join(temp_dir, 'frame_%05d.png'),
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
                    '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart',
                    '-y', str(output_path)
                ]
                subprocess.run(cmd, check=True, capture_output=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ FFmpeg недоступен, используется OpenCV")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(str(output_path), fourcc, self.fps,
                                     (self.width, self.height))
                if out.isOpened():
                    for frame_num in range(frames_needed):
                        frame_file = os.path.join(temp_dir, f"frame_{frame_num:05d}.png")
                        frame = cv2.imread(frame_file)
                        if frame is not None:
                            out.write(frame)
                    out.release()
                else:
                    raise RuntimeError("Не удалось создать видеофайл")
            
            if output_path.exists():
                size = output_path.stat().st_size
                print(f"✅ Видео сохранено: {output_path}")
                print(f"📊 Размер: {size} байт ({size/1024/1024:.2f} MB)")
                return True
            return False
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class YouTubeDecoder:
    def __init__(self, key: Optional[str] = None):
        self.width = 1920
        self.height = 1080
        self.block_height = 16
        self.block_width = 24
        self.spacing = 4
        self.marker_size = 80
        
        if key and key.strip():
            self.key = hashlib.sha256(key.encode()).digest()
        else:
            self.key = None
        
        self.colors = {
            '0000': (255, 0, 0), '0001': (0, 255, 0),
            '0010': (0, 0, 255), '0011': (255, 255, 0),
            '0100': (255, 0, 255), '0101': (0, 255, 255),
            '0110': (255, 128, 0), '0111': (128, 0, 255),
            '1000': (0, 128, 128), '1001': (128, 128, 0),
            '1010': (128, 0, 128), '1011': (0, 128, 0),
            '1100': (128, 0, 0), '1101': (0, 0, 128),
            '1110': (192, 192, 192), '1111': (255, 255, 255)
        }
        
        self.color_values = np.array(list(self.colors.values()), dtype=np.int32)
        self.color_keys = list(self.colors.keys())
        self.color_cache = {}
        
        self.blocks_x = (self.width - 2*self.marker_size) // (self.block_width + self.spacing)
        self.blocks_y = (self.height - 2*self.marker_size) // (self.block_height + self.spacing)
        self.blocks_per_region = self.blocks_x * self.blocks_y
        
        self._precompute_coordinates()
    
    def _precompute_coordinates(self):
        self.block_coords = []
        for idx in range(self.blocks_per_region):
            y = idx // self.blocks_x
            x = idx % self.blocks_x
            if y < self.blocks_y:
                cx = self.marker_size + x * (self.block_width + self.spacing) + self.block_width // 2
                cy = self.marker_size + y * (self.block_height + self.spacing) + self.block_height // 2
                self.block_coords.append((cx, cy))
    
    def _decrypt_data(self, data: bytes) -> bytes:
        if not self.key:
            return data
        
        result = bytearray()
        key_len = len(self.key)
        for i, byte in enumerate(data):
            result.append(byte ^ self.key[i % key_len])
        return bytes(result)
    
    def _color_to_bits(self, color: np.ndarray) -> str:
        color_key = (int(color[0]), int(color[1]), int(color[2]))
        
        if color_key in self.color_cache:
            return self.color_cache[color_key]
        
        if color[0] > 200 and color[1] < 50 and color[2] < 50:
            self.color_cache[color_key] = '0000'
            return '0000'
        
        color_arr = np.array([color[0], color[1], color[2]], dtype=np.int32)
        distances = np.sum((self.color_values - color_arr) ** 2, axis=1)
        best_idx = np.argmin(distances)
        result = self.color_keys[best_idx]
        
        self.color_cache[color_key] = result
        return result
    
    def decode_frame(self, frame: np.ndarray) -> list:
        if frame.shape[1] != self.width or frame.shape[0] != self.height:
            frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
        
        blocks = []
        h, w = frame.shape[:2]
        
        for cx, cy in self.block_coords:
            if cx < w and cy < h:
                color = frame[cy, cx]
                bits = self._color_to_bits(color)
                blocks.append(bits)
            else:
                blocks.append('0000')
        
        return blocks
    
    def _blocks_to_bytes(self, blocks: list) -> bytes:
        all_bits = ''.join(blocks)
        bytes_data = bytearray()
        
        for i in range(0, len(all_bits) - 7, 8):
            byte_str = all_bits[i:i+8]
            if len(byte_str) == 8:
                try:
                    byte = int(byte_str, 2)
                    bytes_data.append(byte)
                except ValueError:
                    bytes_data.append(0)
        
        return bytes(bytes_data)
    
    def _find_eof_marker(self, data: bytes) -> int:
        eof_bytes = b'\xe2\x96\x88' * 64
        
        for i in range(len(data) - len(eof_bytes) + 1):
            if data[i:i+len(eof_bytes)] == eof_bytes:
                return i
        return -1
    
    def decode(self, video_file: str, output_dir: str = ".") -> bool:
        video_path = Path(video_file).resolve()
        if not video_path.exists():
            print(f"❌ Файл не найден: {video_file}")
            return False
        
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print("❌ Не удалось открыть видео")
            return False
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"📥 Декодирование: {total_frames} кадров")
        
        all_blocks = []
        
        for frame_num in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_num % 100 == 0:
                print(f"  Прогресс: {frame_num}/{total_frames}")
            
            frame_blocks = self.decode_frame(frame)
            all_blocks.extend(frame_blocks)
        
        cap.release()
        
        bytes_data = self._blocks_to_bytes(all_blocks)
        
        eof_pos = self._find_eof_marker(bytes_data)
        if eof_pos > 0:
            bytes_data = bytes_data[:eof_pos]
            print(f"✅ Найден маркер конца на позиции {eof_pos}")
        
        data_str = bytes_data[:1000].decode('latin-1', errors='ignore')
        pattern = r'FILE:([^:]+):SIZE:(\d+)\|'
        match = re.search(pattern, data_str)
        
        if match:
            filename = match.group(1)
            filesize = int(match.group(2))
            
            header_str = match.group(0)
            header_bytes = header_str.encode('latin-1')
            header_pos = bytes_data.find(header_bytes)
            
            if header_pos >= 0:
                encrypted_data = bytes_data[header_pos + len(header_bytes):header_pos + len(header_bytes) + filesize]
                
                if self.key:
                    file_data = self._decrypt_data(encrypted_data)
                    print("🔓 Данные расшифрованы")
                else:
                    file_data = encrypted_data
                
                safe_filename = Path(filename).name
                output_file = output_path / safe_filename
                
                counter = 1
                stem = output_file.stem
                suffix = output_file.suffix
                while output_file.exists():
                    output_file = output_path / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                with open(output_file, 'wb') as f:
                    f.write(file_data)
                
                print(f"✅ Файл восстановлен: {output_file}")
                print(f"📏 Размер: {len(file_data)} байт")
                return True
        
        output_file = output_path / "decoded_data.bin"
        with open(output_file, 'wb') as f:
            f.write(bytes_data)
        print(f"💾 Данные сохранены: {output_file}")
        return False


def load_key() -> Optional[str]:
    key_file = Path("key.txt")
    if key_file.exists():
        try:
            key = key_file.read_text(encoding='utf-8').strip()
            if key:
                return key
        except Exception:
            pass
    return None


def main():
    print("\n" + "="*50)
    print("🎥 YouTube File Storage")
    print("="*50)
    
    key = load_key()
    if key:
        print(f"🔑 Ключ загружен из key.txt")
    else:
        print("🔓 Шифрование отключено (key.txt не найден или пуст)")
    
    while True:
        print("\n" + "-"*50)
        print("Выберите действие:")
        print("1. Закодировать файл в видео")
        print("2. Декодировать видео в файл")
        print("3. Выход")
        print("-"*50)
        
        choice = input("\nВведите номер (1-3): ").strip()
        
        if choice == "1":
            print("\n--- Кодирование файла ---")
            input_file = input("Путь к файлу: ").strip().strip('"\'')
            
            if not input_file:
                print("❌ Путь не указан")
                continue
            
            default_output = Path(input_file).stem + ".mp4"
            output_file = input(f"Имя выходного видео [{default_output}]: ").strip().strip('"\'') or default_output
            
            encoder = YouTubeEncoder(key)
            encoder.encode(input_file, output_file)
            
        elif choice == "2":
            print("\n--- Декодирование видео ---")
            video_file = input("Путь к видеофайлу: ").strip().strip('"\'')
            
            if not video_file:
                print("❌ Путь не указан")
                continue
            
            output_dir = input("Папка для сохранения [.]: ").strip().strip('"\'') or "."
            
            decoder = YouTubeDecoder(key)
            decoder.decode(video_file, output_dir)
            
        elif choice == "3":
            print("\n👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор. Введите 1, 2 или 3")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()