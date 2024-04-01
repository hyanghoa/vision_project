"use client";
import axios from "axios";
import { useState } from "react";

export default function Home() {
  const [inferenceResponse, setInferenceResponse] = useState(null);

  async function requestInference(formData: FormData) {
    const url = "/inference";
    try {
      const response = await axios.post(url, formData, {});
      setInferenceResponse(response.data); // 응답 데이터를 상태로 설정합니다.
    } catch (error) {
      console.error("Error creating invoice:", error);
    }
  }

  function handleFormSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    requestInference(formData);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <form action="" onSubmit={handleFormSubmit}>
        <input
          name="file"
          type="file"
          multiple
          accept="image/*"
          className="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
        />
        <button
          type="submit"
          className="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
        >
          파일 업로드
        </button>
      </form>
      {inferenceResponse && (
        <div>
          <h2>응답:</h2>
          <pre>{JSON.stringify(inferenceResponse, null, 2)}</pre>
        </div>
      )}
      hello classify menu
    </main>
  );
}
