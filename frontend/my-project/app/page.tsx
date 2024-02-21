import Image from "next/image";
import ImageList from "../components/inference/inference";


export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <ImageList/>
    </main>
  );
}