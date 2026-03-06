"use client";
import { useRef } from "react";
import { Button } from "./ui/button";
import Image from "next/image";
import { uploadDocument } from "../lib/api";
import toast from "react-hot-toast";

export default function UploadButton() {
  const inputRef = useRef(null);

  const handleClick = () => inputRef.current.click();

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const res = await uploadDocument(file);
      toast.success(`File ${res.filename} uploaded!`);
    } catch (err) {
      console.log("error uploading file");
      console.log(err);

      toast.error("Error uploading file");
    }
  };

  return (
    <>
      <input
        type="file"
        ref={inputRef}
        style={{ display: "none" }}
        accept=".pdf,.txt,.md"
        onChange={handleFileChange}
      />
      <Button className="rounded-full h-10 w-10 p-1" onClick={handleClick}>
        <Image src="/doc.svg" alt="Upload" width={40} height={40} />
      </Button>
    </>
  );
}