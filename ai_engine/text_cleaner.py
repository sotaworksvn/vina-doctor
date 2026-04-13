1. Trách nhiệm (Responsibility)
Module text_cleaner.py là lớp bảo mật trung gian (Firewall). Nhiệm vụ cốt lõi là nhận diện và ẩn danh hóa các thông tin định danh cá nhân (PII - Personally Identifiable Information) từ bản transcript thô trước khi dữ liệu được gửi đến các mô hình ngôn ngữ lớn (LLM) hoặc lưu trữ lâu dài.

2. Cách dùng (Usage)
Được sử dụng như một filter bắt buộc trong AI Pipeline để đảm bảo tuân thủ tiêu chuẩn HIPAA/GDPR.

from ai_engine.processors.text_cleaner import PrivacyGuard

guard = PrivacyGuard()
safe_text = guard.anonymize_transcript(raw_transcript)


3. Các hàm chính (Main Functions)
extract_entities(text): Sử dụng mô hình NER (Named Entity Recognition) để tìm tên người, số điện thoại, địa chỉ, số CMND/CCCD.

mask_pii(text): Thay thế các thực thể nhạy cảm bằng nhãn ẩn danh (ví dụ: "Nguyễn Văn A" -> "[PATIENT_NAME]").

medical_term_fixer(text): Chuẩn hóa các từ viết tắt hoặc lỗi chính tả của các thuật ngữ y khoa phổ biến để hỗ trợ Agent trích xuất chính xác hơn.

de_anonymize(text, mapping): (Tùy chọn) Khôi phục thông tin gốc cho bản báo cáo cuối cùng nếu bác sĩ yêu cầu xuất file PDF đầy đủ tên tuổi.

4. Lưu ý bảo mật (Security Notes)
Local Processing: NER nên được chạy local bằng các thư viện như SpaCy hoặc VinAI/PhoBERT để đảm bảo dữ liệu nhạy cảm chưa được gửi đi đâu trước khi làm sạch.

No Logs Policy: Module này tuyệt đối không được ghi log (logging) các nội dung văn bản thô chứa PII của bệnh nhân.

5. Kết nối với các module khác
Input: Nhận văn bản từ audio.md.

Output: Cung cấp dữ liệu "sạch" cho agents/extractor.py để phân tích bệnh lý và tạo báo cáo SOAP.
"""


### Tóm tắt nội dung các module:

1.  **audio.md**: Tập trung vào việc chuyển đổi âm thanh thành văn bản có phân vai (Diarization) sử dụng Qwen2.5-Audio-Turbo. Đây là "cửa ngõ" dữ liệu đầu tiên của hệ thống, chịu trách nhiệm xử lý nhiễu và định danh giọng nói.
2.  **text_cleaner.md**: Đóng vai trò lớp bảo mật PII (Personally Identifiable Information). Module này đảm bảo mọi thông tin nhạy cảm của bệnh nhân được ẩn danh hóa trước khi đưa vào các bước xử lý trí tuệ nhân tạo tiếp theo, giúp dự án tuân thủ các tiêu chuẩn y tế khắt khe.

Các tài liệu này đã được cấu trúc theo đúng yêu cầu: trách nhiệm, cách dùng, hàm chính, bảo mật và khả năng tích hợp, giúp bạn hoàn thiện hồ sơ kỹ thuật cho Challenge 1.