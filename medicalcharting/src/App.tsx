import { useState } from 'react'
import {Textarea} from '@/components/ui/textarea'
import {Button} from '@/components/ui/button'
import axios from 'axios'

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
            <Textarea
              key={key}
              defaultValue={content}

              className="min-h-[400px] flex-1 p-4 md:min-h-[700px] lg:min-h-[700px]"
            />
          </div>
        </div>
      </div>
    </>
  )
}

export default App
