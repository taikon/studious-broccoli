import './Editor.css'
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import { EditorContent, useEditor } from '@tiptap/react'

import * as Y from 'yjs'
import Collaboration from '@tiptap/extension-collaboration'

// Importing the provider
import { TiptapCollabProvider } from '@hocuspocus/provider'

export default () => {
  const doc = new Y.Doc()

  // Connect to your Collaboration server
  const provider = new TiptapCollabProvider({
    name: "document.name", // Unique document identifier for syncing. This is your document name.
    appId: '7j9y6m10', // Your Cloud Dashboard AppID or `baseURL` for on-premises
    token: 'notoken', // Your JWT token
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
    <EditorContent editor={editor} />
  )
}
