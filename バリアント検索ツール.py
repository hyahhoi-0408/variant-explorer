import streamlit as st
import re
import urllib.parse

# 1. アプリのタイトルを表示（ブラウザの大きな見出しになります）
st.title("🧬 Variant Explorer JP")
st.caption("遺伝子バリアントの簡易評価をサポートするツール")

# 2. 入力フォームを作成（「送信」ボタンを押すまで待機する枠組みです）
with st.form("my_form"):
    # ユーザーが文字を打ち込むための箱を3つ作る
    variant_input = st.text_input("バリアント (例: c.7570+5G>A) 💡 (Mutalyzer3, clinvarで使用)", "")
    gene_name = st.text_input("遺伝子名 (例: FBN1) 💡 (NCBI, clinvarで使用)", "")
    reference_number = st.text_input("RefSeqアクセッション番号 (例: NM_000138.5) 💡 (Mutalyzer3で使用)", "")
    Genomic_Description = st.text_input("ゲノム表記 (例: NC_000015.10:g.48421947C>T)  💡 (SpliceAI, CADD, gnomADで使用)", "")
 
    # 解析を開始するためのボタン
    submit_button = st.form_submit_button("解析開始")

# 3. ボタンが押された時の処理
if submit_button:
    if variant_input and gene_name:
        st.write(f"### 🔍 {gene_name}: {variant_input} の解析結果")
    
    elif reference_number:
        st.write(f"### 🔍 {reference_number} の解析結果")
    
    elif  Genomic_Description:
        st.write(f"### 🔍 {Genomic_Description} の解析結果")

    elif gene_name:
        st.write(f"### 🔍 {gene_name} の解析結果")
    
    elif variant_input:
        st.write(f"### 遺伝子名などのほかの項目も入力してください")
    
    else:
        st.warning("いずれかの項目を入力してください")
        
        # 画面を左右2列に分ける
    col1, col2 = st.columns(2)
        
    with col1:
        if gene_name:
        # NCBIでNCとかのやつ探す
             NCBI_url = f"https://www.ncbi.nlm.nih.gov/search/all/?term={gene_name}"
              # 案1：<br> を使って強制改行する（一番シンプル！）
             st.markdown(f"**[NCBIで検索]({NCBI_url})** <small>(転写産物ID取得可能)</small>", unsafe_allow_html=True)
            
        else:      
        # 入力が空っぽの時の警告
             st.warning("NCBIを使用する場合は遺伝子名を入力してください。")

        if reference_number and gene_name:
             Mutalyzer_url = f"https://mutalyzer.nl/normalizer/{reference_number}:{variant_input}"
             st.markdown(f"**[Mutalyzer3で検索]({Mutalyzer_url})**<small>(ゲノム座標取得可能)</small>", unsafe_allow_html=True)
            
        else:
             # 入力が空っぽの時の警告
             st.warning("Mutalyzer3を使用する場合はRefSeqアクセッション番号と遺伝子名の両方を入力してください。")
        
        if variant_input and gene_name:
             ggg = f'"{gene_name}"[GENE] AND "{variant_input}"[VARNAME]'
             safe_query = urllib.parse.quote(ggg)
             clinvar_url = f"https://www.ncbi.nlm.nih.gov/clinvar/?term={safe_query}"
             st.markdown(f"**[ClinVarで検索]({clinvar_url})**")
            
        else:
             # 入力が空っぽの時の警告
             st.warning("ClinVarを使用する場合はバリアントと遺伝子名の両方を入力してください。")
            

        
        with col2:
            if Genomic_Description:
        # 2. 正規表現で「染色体番号」「位置」「リファレンス塩基」「アンバリアント塩基」を抜き出す
        # パターンの意味: NC_ (何かついてる) :g. (数字) (塩基) > (塩基)
             match = re.search(r'NC_0+(\d+)\.\d+:g\.(\d+)([ATGC])>([ATGC])', Genomic_Description)

             if match:
                  chrom = match.group(1)   # 染色体番号（例: 23）
                  pos = match.group(2)     # 位置（例: 153798327）
                  ref = match.group(3)     # 元の塩基（例: A）
                  alt = match.group(4)     # 変わった後の塩基（例: G） 
            
            # 3. SpliceAI用のフォーマットに合体！
                  splice_ai_format = f"{chrom}-{pos}-{ref}-{alt}"
                  # st.success(f"変換成功: `{splice_ai_format}`")
            
            # SpliceAIへのリンク作成
                  splice_url = f"https://spliceailookup.broadinstitute.org/#variant={splice_ai_format}&genome=grch38"
                  st.markdown(f"**[SpliceAIで検索]({splice_url})**")
                  site_chrom = chrom
                 
            # 2. もし数字が「23」だったら、中身を「X」に書き換える
                  if chrom == "23":
                      site_chrom = "X"

            # 3. もし数字が「24」だったら、中身を「Y」に書き換える
                  elif chrom == "24":
                      site_chrom = "Y"
            
             cadd_url = f"https://cadd.gs.washington.edu/snv/{"GRCh38-v1.7"}/{site_chrom}:{pos}_{ref}_{alt}"        
        
            # 元々の [CADDスコアを確認] リンクをこれに書き換える
             st.markdown(f"**[CADDで検索]({cadd_url})**")
        
            # gnomAD: 遺伝子名で検索結果一覧へ
             gnomad_url = f"https://gnomad.broadinstitute.org/variant/{site_chrom}-{pos}-{ref}-{alt}"
             st.markdown(f"**[gnomADで検索]({gnomad_url})**") 

            else:st.warning("SpliceAI, CADD, gnomADを使用する場合は、ゲノム座標をNC_000023.11:g.153798327A>G のような形式で入力してください。")


