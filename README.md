# albert-extensions

Extensions of Albert Launcher

## Albert とは

[Albert](https://albertlauncher.github.io/) は Linux で動く CUI タイプのランチャー。
Mac の spotlight みたいなやつで、軽快に動くしとても好き。
好きなので、Extensionを作ってみた。

## Albert のインストール

以下、Ubuntu（正確には [Lubuntu](https://lubuntu.me/)）を前提とする。
（他のディストリビューションではやってない）

普通に `sudo apt install albert` でも簡単にインストールできるけど、
これだと Python Extension の対応がない古いバージョンしか入らない。（作成当時）

### apt を使ったインストール

以下、情報が古くなっているかもしれないので、 [本家](https://albertlauncher.github.io/docs/installing/) を確認すること。

* `> wget -nv -O Release.key https://build.opensuse.org/projects/home:manuelschneid3r/public_key`
* `> sudo apt-key add - < Release.key`
* `> sudo sh -c "echo 'deb http://download.opensuse.org/repositories/home:/manuelschneid3r/xUbuntu_18.04/ /' > /etc/apt/sources.list.d/home:manuelschneid3r.list"`
* `> sudo apt update`
* `> sudo apt install albert`

### ソースコードからインストール（余談）

これも [本家](https://albertlauncher.github.io/docs/installing/) を確認のこと。

VirtualBox 関係は個人的に使わないので無効化している。

* `> sudo apt install cmake qtbase5-dev libqt5x11extras5-dev libqt5svg5-dev qtdeclarative5-dev`
* `> git clone --recursive https://github.com/albertlauncher/albert.git`
* `> mkdir albert-build`
* `> cd albert-build`
* `> cmake ../albert -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_VIRTUALBOX=OFF -DCMAKE_BUILD_TYPE=Release`
* `> make`
* `> sudo make install`

## Albert の Python プラグイン

Albert を起動し、設定画面の "Extensions" "Python" にチェックを入れると有効になる。

有効化し、さらに右ペインに Extension 一覧が出てくるので、好きなものにチェックを入れて有効化する。

本家で作っているPython Extensionは `/usr/share/albert/org.albert.extension.python/modules` 以下に入っている。

基本的には [このGitHubリポジトリ](https://github.com/albertlauncher/python) と同じものが入る。
（作成時点でなぜかAtomProject.pyが入らない。非常に便利なのでなんとかしてほしい。まぁ手動で入れればいいだけの話だが）

個人で作った Extension は `~/.local/share/albert/org.albert.extension.python/modules` 以下のものが Albert 本体に認識される。
要するに、このリポジトリの modules ディレクトリを上記のディレクトリにシンボリックリンク貼ることで、インストールしたことになる。

`/usr/share/...` の Extension も `~/.local/share/...` の Extension も同列に扱われる。

## Albert をオフライン簡易英和/和英辞書 Viewer にしよう

そもそも私の「Albert の Extension を作りたい」という動機が、
「Albert をオフライン簡易英和/和英辞書 Viewer にしたい」という欲望からくるものだった。

本格的な辞書および辞書 Viewer は「英辞郎の StarDict 形式化」とか「 [GoldenDict](http://goldendict.org/) 」に任せ、
Albert を「単語を入力するとオフラインで検索して（代表的な）訳語がひとつ返ってくるような簡易英和/和英辞書 Viewer」として使いたい。

### 無料英和/和英辞書データの入手とデータ形式の変換

それにはまず無料の辞書データを入手しなければならない。

まず英和辞書であるが、GENE95辞書というものがあるらしい。
しかしその配布本家である Namazu.org が現時点では消滅している。
なので、とあるサイトから StarDict 形式のデータをダウンロードしてきた。

これを単純なテキスト形式に変換する。

* ダウンロードしたデータを展開
    * `> tar jxvf stardict-ej-gene95-x.x.x.tar.bz2`
* stardict形式をtextに変換するために、stardict-toolsをインストールする
    * `> sudo apt install stardict-tools`
* stardict-editor を起動して、text に変換する
    * `> cd stardict-ej-gene95-x.x.x`
    * `> cp ej-gene95.dict.dz ej-gene95.dict.gz`
    * `> gunzip ej-gene95.dict.gz`
    * `> stardict-editor`
    * "DeCompile/Verify" を選ぶ
    * Filename に ej-gene95.ifo を選択
    * 左下が "Tab file" になっていることを確認し、"Decompile"
* `ej-gene95.txt` が完成

作成された `ej-gene95.txt` は、行の先頭に英単語があり、タブ区切りの後、和訳が `,` 区切りで書かれている形式である。

次に和英辞書であるが、 [JMdict/EDICT Project](http://www.edrdg.org/jmdict/edict_doc.html) から JMdict_e.gz をダウンロードした。
解凍した中身は XML ファイルである。 これを上記と同じようなフォーマットに変換したい。

そこで [変換スクリプト](script/jmdict2txt.py) を用意した。
JMdict は頻繁に更新されるらしいので、これがいつまで動くかは分からないが。

先に作った `ej-gene95.txt` と上記で作った `je-jmdict.txt` は `/usr/local/share/dict/` ディレクトリ下に置くことにする。

## 本リポジトリに入っている Extension の概要

* EJ_Dictionary.py
    * GENE95 辞書を使った英和辞書
    * ag（ [The Silver Searcher](https://github.com/ggreer/the_silver_searcher) ）が必要
        * `> suto apt install silversearcher_ag`
    * トリガーは `ej`
        * Albert に `ej ` （最後のスペース必要）と入力すると、英和辞書が発動する
    * `ej-gene95.txt` から前方一致で探す
    * 単語がひとつに定まると、複数の訳語がある場合それらをさらに分解して表示する
    * 表示された訳を Albert 上で選択すると、それが ClipBoard にコピーされる
    * 入力を `'` もしくは `"` で囲むと、完全一致で探す
* JE_Dictionaly.py
    * JMdict 辞書を使った和英辞書
    * トリガーは `je`
    * 後は EJ_Dictionary.py と同じ
* ScrotDesktop.py
    * 本家の [Scrot.py](https://github.com/albertlauncher/python/blob/master/Scrot.py) に*インスパイア*されて作った
    * トリガーは `ss`
    * 本家は Pictures フォルダに画像を入れるが、これはデスクトップに置く
    * ５種類（画面全体・マルチスクリーンの画面全体・選択範囲・ウィンドウ・枠なしウィンドウ）を明示的に表示
    * キーボード入力でも上記５種類を選択できるように
