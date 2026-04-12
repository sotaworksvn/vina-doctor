# vina-doctor

Theo cách chia 3 khối frontend, backend, ai_engine của dự án này, tôi sẽ đặt như sau:

**Phân Vai Trách Nhiệm**

1. Client record audio: frontend
   Frontend chịu trách nhiệm xin quyền microphone, ghi âm, hiển thị trạng thái thu, và upload file hoặc stream audio lên API.

2. Gửi audio lên FastAPI: `frontend -> backend`
   Frontend chỉ gọi HTTP/WebSocket tới FastAPI. Điểm nhận request phải nằm ở backend, không đặt ở ai_engine.

3. FastAPI đẩy sang DashScope để lấy Transcript + Diarization: chia 2 lớp
   backend: orchestration, auth, request lifecycle, retry, timeout, logging, job status.
   ai_engine: logic AI/audio, adapter gọi DashScope Qwen2.5-Audio, chuẩn hóa transcript, diarization mapping.
   
   Nói ngắn gọn: backend điều phối, ai_engine xử lý AI.

4. FastAPI gửi Transcript + Master Prompt sang Qwen Max để trích xuất báo cáo: cũng chia 2 lớp
   backend: nhận transcript, gọi pipeline trích xuất, kiểm soát schema đầu ra, lưu trạng thái.
   ai_engine: prompt management, extraction logic, gọi Qwen Max, validate/normalize JSON báo cáo.

5. Database lưu kết quả: backend
   Database là phần hạ tầng của backend. Backend nên là nơi duy nhất đọc/ghi DB để giữ transaction, authz, audit log, versioning của report.

6. Client nhận JSON và render báo cáo đa ngôn ngữ đẹp mắt: frontend
   Frontend nhận JSON đã chuẩn hóa từ backend rồi render thành report viewer, timeline hội thoại, speaker segments, multilingual tabs, export PDF nếu cần.

**Quy Tắc Kiến Trúc Nên Giữ**

- frontend chỉ lo UX: record, upload, polling/realtime updates, render kết quả.
- backend là cổng vào duy nhất: API, auth, DB, job orchestration, queue/background task.
- ai_engine là domain AI thuần: STT, diarization, prompt, extraction, normalization, multilingual generation.
- `database` thuộc backend/infrastructure, không cho frontend hay ai_engine ghi trực tiếp.

**Map Theo Luồng Hoàn Chỉnh**

frontend -> thu âm, upload, hiển thị tiến trình  
backend -> nhận audio, tạo consultation/job, gọi ai_engine  
ai_engine -> gọi DashScope Audio, lấy transcript + diarization  
ai_engine -> gọi Qwen Max với master prompt, trả structured report  
backend -> lưu DB, trả JSON chuẩn hóa  
frontend -> render báo cáo đa ngôn ngữ

Từ tài liệu hiện có của repo, cách chia này cũng khớp với hướng dẫn trong vina-doctor-agent.md và workflow tổng quát trong workflow.md.

Nếu cần, tôi có thể làm tiếp 1 trong 2 việc sau:
1. Vẽ lại sơ đồ component/data flow chuẩn cho repo này.
2. Đề xuất luôn cấu trúc thư mục/API endpoint/job schema cụ thể cho 3 khối.