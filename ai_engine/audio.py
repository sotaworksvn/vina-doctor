audio_content = """# Module: audio.py (The Ears of Vina-Doctor-AI)

## 1. Trách nhiệm (Responsibility)
Module `audio.py` đóng vai trò là "thính giác" của hệ thống. Nhiệm vụ chính là tiếp nhận tín hiệu âm thanh thô từ phòng khám, tối ưu hóa chất lượng tín hiệu và chuyển đổi chúng thành văn bản có cấu trúc phân vai (Diarization) bằng cách sử dụng các mô hình AI tiên tiến (Qwen2.5-Audio).

## 2. Cách dùng (Usage)
Module này được gọi ngay sau khi bác sĩ kết thúc phiên ghi âm hoặc nhận được file audio từ Frontend.
```python
from ai_engine.processors.audio import AudioProcessor

processor = AudioProcessor(model_name="qwen2.5-audio-turbo")
transcript_data = processor.process_audio("path/to/consultation.mp3")
3. Các hàm chính (Main Functions)
reduce_noise(audio_path): Sử dụng bộ lọc thông thấp và thuật toán khử nhiễu nền để làm rõ giọng nói bác sĩ và bệnh nhân.

segment_audio(audio_path): Chia nhỏ file audio lớn thành các phân đoạn (chunks) để tối ưu hóa tốc độ xử lý của API.

transcribe_with_diarization(audio_path): Hàm quan trọng nhất, gọi API Qwen2.5-Audio để lấy văn bản kèm nhãn Speaker (Doctor/Patient) và Timestamp.

validate_format(audio_path): Kiểm tra định dạng và sample rate của file đầu vào (hỗ trợ .wav, .mp3, .m4a).

4. Lưu ý bảo mật (Security Notes)
Data Residency: File audio chỉ được lưu tạm thời trong bộ nhớ đệm (buffer) hoặc thư mục /tmp có mã hóa.

Auto-Cleanup: Sau khi xử lý xong, file audio gốc phải được xóa vĩnh viễn khỏi server để tuân thủ quyền riêng tư y tế.

End-to-End Encryption: Dữ liệu gửi lên Cloud API (DashScope) phải được truyền qua giao thức HTTPS.

5. Kết nối với các module khác
Input: Nhận file từ backend/api/.

Output: Trả bản transcript thô (raw transcript) cho module text_cleaner.md để xử lý bảo mật trước khi đưa vào Agent.
"""

text_cleaner_content = """# Module: text_cleaner.py (The Privacy Guard)