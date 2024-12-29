import { useState } from "react";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) return alert("Please upload a CAPTCHA image!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/solve_captcha", {
        method: "POST",
        body: file,
      });
      const data = await response.json();
      setResult(data.captcha_text || "Error solving CAPTCHA");
    } catch (error) {
      setResult("Error solving CAPTCHA");
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit">Solve CAPTCHA</button>
      </form>
      {result && <p>Result: {result}</p>}
    </div>
  );
}