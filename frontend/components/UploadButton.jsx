"use client";
import { useRef, useState } from "react";
import { Button } from "./ui/button";
import Image from "next/image";
import { uploadDocument } from "../lib/api";
import toast from "react-hot-toast";

export default function UploadButton() {
  const inputRef = useRef(null);
  const [loading, setLoading] = useState(false);

  const handleClick = () => inputRef.current.click();

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    try {
      const res = await uploadDocument(file);
      toast.success(`File ${res.filename} uploaded!`);
    } catch (err) {
      console.log("error uploading file");
      console.log(err);
      toast.error("Error uploading file");
    } finally {
      setLoading(false);
      e.target.value = "";
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
      <Button
        className="rounded-full h-10 w-10 p-1"
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? (
          <svg
            className="animate-spin h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        ) : (
          <Image src="/doc.svg" alt="Upload" width={40} height={40} />
        )}
      </Button>
    </>
  );
}