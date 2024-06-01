import { useState } from 'react'
import {Button} from '@/components/ui/button'
import axios from 'axios'

import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import { EditorContent, useEditor } from '@tiptap/react'

import * as Y from 'yjs'
import Collaboration from '@tiptap/extension-collaboration'

import { TiptapCollabProvider } from '@hocuspocus/provider'

import FileUploadDropzone from '@/components/custom/file-upload-dropzone'
import {Toaster} from 'sonner'

function App() {
  const [text, setText] = useState('')

  function handleClear() {
    if (!editor) {
      return
    }
    editor.commands.clearContent()
  }

  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleCreateMessage() {
    if (!editor) {
      return
    }

    setIsSubmitting(true); // Disable button when the POST request starts

    const createMessageUrl = import.meta.env.VITE_FASTAPI_SERVER_API_BASE_URL + '/api/messages'

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

      if (response.data) {
        editor.commands.setContent(response.data.prediction)
      }
    } catch (error) {
      console.error(error)
    } finally {
      setIsSubmitting(false); // Enable button when the POST request ends
    }
  }

  const doc = new Y.Doc() // Initialize Y.Doc for shared editing

  // Connect to your Collaboration server
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

  function handleClick() {
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
              <Button onClick={handleCreateMessage} disabled={isSubmitting}>
                {isSubmitting ? "Creating..." : "Create Message"}
              </Button>
              <Button onClick={handleClick}>Set Content</Button>
            </div>
          </div>

          <div className="flex-1 py-16">
            <div className="container h-full py-6">
              <FileUploadDropzone />
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

export default App
