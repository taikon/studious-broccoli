import { useState } from 'react'
import axios from 'axios'

import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import { EditorContent, useEditor } from '@tiptap/react'

import * as Y from 'yjs'
import Collaboration from '@tiptap/extension-collaboration'

import { TiptapCollabProvider } from '@hocuspocus/provider'

import { Button } from '@/components/ui/button'
import { Toaster, toast } from "sonner";
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import './App.css'

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
      // setFiles(Array.from(event.target.files));
      setFiles(prevFiles => [...prevFiles, ...Array.from(event.target.files)]);
    } else {
      setFiles([]); // Handle null case
    }
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!editor) {
      return
    }

    if (files.length === 0) {
      toast.error("No files selected");
      return;
    }

    toast.info("Processing data");
    const uploadUrl = import.meta.env.VITE_FASTAPI_SERVER_API_BASE_URL + '/api/upload'
    const authorization = "Bearer " + import.meta.env.VITE_FASTAPI_SERVER_ACCESS_TOKEN;

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await axios.post(uploadUrl, formData, {
        method: "POST",
        headers: { 
          Authorization: authorization,
          'Content-Type': 'multipart/form-data',
        },
        data: formData
      });

      if (response.status === 200) {
        const prediction = response.data.prediction;
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

  function handleResetFiles() {
    if (!editor) {
      return
    }

    setFiles([]);
  }

  if (editor) {
    return (
      <>
        <div className="h-full flex-col md:flex">
          <div className="container flex flex-col items-start justify-between space-y-2 py-4 sm:flex-row sm:items-center sm:space-y-0 md:h-16">
            <h2 className="text-lg font-semibold">Assist</h2>
            <div className="ml-auto flex w-full space-x-2 sm:justify-end">
              <Button onClick={handleClear}>Clear</Button>
              <Button onClick={handleResetFiles}>Reset Files</Button>
            </div>
          </div>

          <div className="flex-1">
            <div className="container h-full py-6">

              <form onSubmit={handleSubmit}>
                <Label className='pl-1'>Upload files</Label>
                <div className="flex w-full max-w-sm items-center space-x-2 cursor-pointer">
                  <Input 
                    type="file" 
                    multiple 
                    accept="image/*"
                    onChange={handleFileChange} 
                    capture="environment"
                    className='hover:bg-neutral-100 outline-dashed outline-1 outline-white rounded-lg cursor-pointer'
                  />
                  <Button type="submit">Summarize</Button>
                </div>
              </form>
              {files.length > 0 && (
                <div>
                  <ul>
                    {files.map((file, index) => (
                      <li key={index}>{file.name}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          <div className="flex-1">
            <div className="container h-full py-6">
              <EditorContent editor={editor} />
            </div>
          </div>
        </div>
        <Toaster />
      </>
    )
  }
}

export default App;
