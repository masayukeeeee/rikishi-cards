import Head from "next/head";
import RikishiCard from './components/RikishiCard';
import rikishiData from './data/2025_hatsubasho_rikishi.json';
import { RikishiData } from './types/rikishi';

const typedRikishiData = rikishiData as RikishiData; // 型アサーションを追加

export default function Home() {
  return (
    <>
      {/* ページタイトルを設定 */}
      <Head>
        <title>力士カード一覧 - 2025年初場所</title>
        <meta name="description" content="2025年初場所の力士プロフィール情報をカード形式で表示します。" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      {/* ページ冒頭のタイトル */}
      <div className="p-4">
        <h1 className="text-3xl font-bold text-center mb-6">
          力士カード一覧 - 2025年初場所
        </h1>
      </div>

      {/* 力士カード一覧 */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4">
        {Object.keys(rikishiData).map((key) => {
          const rikishi = typedRikishiData[key];
          return (
            <RikishiCard
              key={key}
              name={rikishi.name}
              rank={rikishi.detail.rank_detail}
              fullName={rikishi.detail.full_name}
              fullNameKana={rikishi.detail.full_name_hiragana}
              heya={rikishi.heya}
              imageUrl={rikishi.profile_img.image_url}
            />
          );
        })}
      </div>
    </>
  );
}