"use client";

import Image from 'next/image';
import { useCallback } from 'react';

interface RikishiCardProps {
  name: string;
  rank: string;
  fullName: string;
  fullNameKana: string;
  heya: string;
  imageUrl: string;
}

export default function RikishiCard({
  name,
  rank,
  fullName,
  fullNameKana,
  heya,
  imageUrl,
}: RikishiCardProps) {
  const speakText = useCallback(() => {
    const speech = new SpeechSynthesisUtterance();
    speech.text = `${fullNameKana}`;
    speech.lang = 'ja-JP'; // 日本語
    window.speechSynthesis.speak(speech);
  }, [fullNameKana]);

  return (
    <div
      className="border rounded-lg shadow-md p-4 text-center bg-white max-w-sm cursor-pointer hover:shadow-lg transition-shadow duration-300"
      onClick={speakText} // カード全体をクリックしたときに読み上げ
    >
      <Image
        src={imageUrl}
        alt={name}
        width={200}
        height={300}
        className="rounded-lg mb-4 mx-auto"
      />
      <h2 className="text-xl font-bold text-black">
        {fullName}
      </h2>
      <p className="text-gray-500">{rank}</p>
      <p className="text-sm text-gray-500">{heya} 部屋</p>
    </div>
  );
}