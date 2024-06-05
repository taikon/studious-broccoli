import { useState } from 'react'
import axios from 'axios'

import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import { EditorContent, useEditor } from '@tiptap/react'

import * as Y from 'yjs'
import Collaboration from '@tiptap/extension-collaboration'

import { TiptapCollabProvider } from '@hocuspocus/provider'

import FileUploadDropzone from '@/components/custom/file-upload-dropzone'
import {Button} from '@/components/ui/button'
import { Toaster, toast } from "sonner";

function App() {
  function handleClear() {
    if (!editor) {
      return
    }
    editor.commands.clearContent()
  }

  async function handleCreateMessage(text: string) {
    if (!editor) {
      return
    }

    const createMessageUrl = import.meta.env.VITE_FASTAPI_SERVER_API_BASE_URL + '/api/message'

    const headers = {
      "Content-Type": "application/json",
      Authorization: "Bearer " + import.meta.env.VITE_FASTAPI_SERVER_ACCESS_TOKEN,
    };

    try {
      const response = await axios.post(
        createMessageUrl,
        {
          prompt: text
        },
        { headers }
      )

      if (response.status === 200 || response.status === 201) {
        editor.commands.setContent(response.data.prediction)
        toast.success("Message created successfully");
      } else {
        toast.error("Failed to create message");
      }
    } catch (error) {
      console.error(error)
    }
  }

  const [files, setFiles] = useState<File[]>([]);

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>): void {
    if (event.target.files !== null){
      setFiles(Array.from(event.target.files));
    } else {
      setFiles([]); // Handle null case
    }
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!editor) {
      return
    }

    toast.info("Processing data");
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
        const prediction = result.prediction;
        toast.success("File uploaded successfully, starting summarization");
        handleCreateMessage(prediction);
      } else {
        toast.error("Failed to upload file");
      }
    } catch (error) {
      console.error(error);
    }
  }

  // Initialize Y.Doc for shared editing
  const doc = new Y.Doc() 

  // Connect to your Collaboration server
  // @ts-ignore
  const provider = new TiptapCollabProvider({ 
    name: "document.name",
    appId: import.meta.env.VITE_TIPTAP_COLLAB_APP_ID, 
    token: import.meta.env.VITE_TIPTAP_JWT,
    document: doc,
  })

  const editor = useEditor({
    extensions: [
      Document,
      Paragraph,
      Text,
      Collaboration.configure({
        document: doc,
      }),
    ],
    content: `
      <p></p>
    `,
  })

  function handleResetContent() {
    if (!editor) {
      return
    }

    editor.commands.setContent('Hello World')
  }

  if (editor) {
    return (
      <>
        <div className="hidden h-full flex-col md:flex">
          <div className="container flex flex-col items-start justify-between space-y-2 py-4 sm:flex-row sm:items-center sm:space-y-0 md:h-16">
            <h2 className="text-lg font-semibold">Application</h2>
            <div className="ml-auto flex w-full space-x-2 sm:justify-end">
              <Button onClick={handleClear}>Clear</Button>
              <Button onClick={handleResetContent}>Set Content</Button>
            </div>
          </div>

          <div className="flex-1 py-16">
            <div className="container h-full py-6">
              <FileUploadDropzone />
            </div>
          </div>

          <div className="flex-1 py-16">
            <div className="container h-full py-6">

              <div>
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

            </div>
          </div>

          <div className="flex-1">
            <div className="container h-full py-6">
              <EditorContent editor={editor} className='ring-1 ring-gray-500 rounded-lg lg:h-[500px] md:h-[500px] sm:h-[300px] h-[300px]' />
            </div>
          </div>
        </div>
        <Toaster />
      </>
    )
  }
}

export default App;
