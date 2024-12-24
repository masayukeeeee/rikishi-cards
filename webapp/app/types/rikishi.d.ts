// app/types/rikishi.d.ts
export interface RikishiDetail {
  full_name: string;
  full_name_hiragana: string;
  rank_detail: string;
}

export interface RikishiProfileImage {
  url: string;
  image_url: string;
  local_path: string;
}

export interface Rikishi {
  basho: string;
  name: string;
  profile_url: string;
  country: string;
  country_url: string;
  heya: string;
  heya_url: string;
  profile_img: RikishiProfileImage;
  detail: RikishiDetail;
}

export type RikishiData = {
  [key: string]: Rikishi; // キーが文字列であることを指定
};
