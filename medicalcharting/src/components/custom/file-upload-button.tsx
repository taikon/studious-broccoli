import {useState} from "react";
import {Button} from "@/components/ui/button";

function FileUploadButton() {
  const [files, setFiles] = useState([]);

  function handleFileChange(event) {
    setFiles(Array.from(event.target.files));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const uploadUrl = import.meta.env.VITE_FASTAPI_SERVER_API_BASE_URL + '/api/upload'
    const authorization = "Bearer " + import.meta.env.VITE_FASTAPI_SERVER_ACCESS_TOKEN;

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await fetch(uploadUrl, {
        method: "POST",
        headers: { 
          Authorization: authorization,
        },
        body: formData
      });

      if (response.status === 200) {
        const result = await response.json();
        console.log(`File uploaded successfully: ${result}`);
      } else {
        console.error("Failed to upload file");
      }
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="ring">
      <form onSubmit={handleSubmit}>
        <input type="file" multiple onChange={handleFileChange} />
        <Button type="submit">Upload</Button>
      </form>
      {files.length > 0 && (
        <div>
          <ul>
            {files.map((file) => (
              <li key={file.name}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default FileUploadButton;
