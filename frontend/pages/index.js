import Head from "next/head";
import UploadForm from "../components/UploadForm";

export default function Home() {
  return (
    <div>
      <Head>
        <title>CAPTCHA Solver</title>
        <meta name="description" content="Upload CAPTCHA to get text solved" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>CAPTCHA Solver</h1>
        <UploadForm />
      </main>
    </div>
  );
}