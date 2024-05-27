import { useState } from 'react'
import {Textarea} from '@/components/ui/textarea'
import {Button} from '@/components/ui/button'
import axios from 'axios'

import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import { EditorContent, useEditor } from '@tiptap/react'

import * as Y from 'yjs'
import Collaboration from '@tiptap/extension-collaboration'

import { TiptapCollabProvider } from '@hocuspocus/provider'

function App() {
  const [content, setContent] = useState('')
  const [key, setKey] = useState(0)

  function handleClear() {
    setKey(key + 1)
  }

  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleCreateMessage() {
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
          prompt: content
        },
        { headers }
      )

      if (response.data) {
        setContent(response.data.prediction)
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
    name: "document.name", // Unique document identifier for syncing. This is your document name.
    // appId: import.meta.env.VITE_TIPTAP_COLLAB_APP_ID, 
    appId: '7j9y6m10', // Cloud Dashboard AppID 
    token: 'notoken', // JWT token
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
      <p>
        This is a radically reduced version of tiptap. It has support for a document, with paragraphs and text. That’s it. It’s probably too much for real minimalists though.
      </p>
      <p>
        The paragraph extension is not really required, but you need at least one node. Sure, that node can be something different.
      </p>
    `,
  })

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
          </div>

        </div>
        <div className="flex-1">
          <div className="container h-full py-6">
            {/* <Textarea */}
            {/*   key={key} */}
            {/*   defaultValue={content} */}
            {/**/}
            {/*   className="min-h-[400px] flex-1 p-4 md:min-h-[700px] lg:min-h-[700px]" */}
            {/* /> */}
          </div>
        </div>
      </div>
    <EditorContent editor={editor} className='ring-1 ring-gray-500' />
    </>
  )
}

export default App
