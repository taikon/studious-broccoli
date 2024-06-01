import {
  FileUploader,
  FileInput,
  FileUploaderContent,
  FileUploaderItem,
} from "@/components/extension/file-upload";
import { DropzoneOptions } from "react-dropzone";
import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Form, FormField, FormItem, FormMessage } from "@/components/ui/form";
import { Button, buttonVariants } from "@/components/ui/button";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";
import { Paperclip, Send } from "lucide-react";
import { cn } from "@/lib/utils";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import axios from "axios";

const CardForm = z.object({
  message: z.string(),
  files: z
    .array(
      z.instanceof(File).refine((file) => file.size < 4 * 1024 * 1024, {
        message: "File size must be less than 4MB",
      })
    )
    .max(5, {
      message: "Maximum 5 files are allowed",
    })
    .nullable(),
});

type CardFormType = z.infer<typeof CardForm>;

const FileUploadDropzone = () => {
  const form = useForm<CardFormType>({
    resolver: zodResolver(CardForm),
    defaultValues: {
      message: "",
      files: null,
    },
  });

  const dropzone = {
    multiple: true,
    maxFiles: 3,
    maxSize: 4 * 1024 * 1024,
  } satisfies DropzoneOptions;

  async function onSubmit(data: CardFormType) {
    toast.success("Processing data");

    const uploadUrl = import.meta.env.VITE_FASTAPI_SERVER_API_BASE_URL + '/api/upload'

    const formData = new FormData();

    if (data.files) {
      data.files.forEach((file) => {
        formData.append("files", file);
      });
    }

    try {
      const response = await fetch(uploadUrl, {
        method: "POST",
        body: formData,
      });

      if (response.status === 200) {
        const result = await response.json();

        toast.success("File uploaded successfully");

        // Log the response data
        console.log(result);

      } else {
        toast.error("Failed to upload file");
      }
    } catch (error) {
      console.error(error);
    }
  }

  console.log(form.getValues("files"));

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="relative w-full grid gap-2 h-12 "
      >
        <div
          className={`w-full flex items-start gap-x-2 rounded-md outline outline-1 outline-border px-2 pb-1 ${
            form.watch("files") !== null ? "pt-4" : "pt-2"
          }`}
        >
          <FormField
            control={form.control}
            name="files"
            render={({ field }) => (
              <FormItem>
                <FileUploader
                  value={field.value}
                  onValueChange={field.onChange}
                  dropzoneOptions={dropzone}
                  reSelect={true}
                >
                  <FileInput
                    className={cn(
                      buttonVariants({
                        size: "icon",
                      }),
                      "size-8"
                    )}
                  >
                    <Paperclip className="size-4" />
                    <span className="sr-only">Select your files</span>
                  </FileInput>
                  {field.value && field.value.length > 0 && (
                    <FileUploaderContent className="absolute bottom-8 p-2  w-full -ml-3 mb-5 rounded-b-none rounded-t-md flex-row gap-2 ">
                      {field.value.map((file, i) => (
                        <FileUploaderItem
                          key={i}
                          index={i}
                          aria-roledescription={`file ${i + 1} containing ${
                            file.name
                          }`}
                          className="p-0 size-20"
                        >
                          <AspectRatio className="size-full">
                            <img
                              src={URL.createObjectURL(file)}
                              alt={file.name}
                              className="object-cover rounded-md w-20 h-20"
                              style={{ objectFit: "cover" }}
                            />
                          </AspectRatio>
                        </FileUploaderItem>
                      ))}
                    </FileUploaderContent>
                  )}
                </FileUploader>
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="message"
            render={({ field }) => (
              <FormItem className="p-0 w-full">
                <Input
                  {...field}
                  className={`border focus-visible:ring-0 border-none w-full`}
                  placeholder="For now this does nothing. But could be used to send a custom prompt to the vision model."
                />
              </FormItem>
            )}
          />
        </div>
        {form.formState.errors && (
          <div className="text-destructive text-sm">
            {Object.values(form.formState.errors).map((error) => (
              <p key={error.message}>{error.message}</p>
            ))}
          </div>
        )}
        <Button type="submit" className="w-fit">
          Send
        </Button>
      </form>
    </Form>
  );
};

export default FileUploadDropzone;
