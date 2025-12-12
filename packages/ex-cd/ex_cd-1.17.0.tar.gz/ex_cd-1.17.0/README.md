# ex-cd

高效下载E站gallery的所有历史数据

* 尽量避免集中数据库，能放进文件夹的数据尽量放进文件夹
* 尽量减少请求操作，能只用读文件的尽量只读文件
* 尽量减少文件读写操作，能只用读文件列表的尽量只读文件列表

## Usage

```sh
python -m ex_cd -c .vscode/config.json https://exhentai.org/g/2635845/ecbc9d9681/
```

```sh
python -m ex_cd -c <a json string> https://exhentai.org/g/2635845/ecbc9d9681/
```

You can see the example config file: `.vscode/config.json`

You can also set an `EXCD_CONFIG_FILE` env to specify a file, and the config in this file will be overridden by the config specified by `-c`:

```sh
export EXCD_CONFIG_FILE=".vscode/config.json"
python -m ex_cd -c <a json string> https://exhentai.org/g/2635845/ecbc9d9681/
```

You can see the example command line: `.vscode/launch.json`

## How does it work?

### URL更新

```mermaid
flowchart TD

UrlCheck1[输入URL] --> UrlCheck2(从URL中提取目标文件夹路径\ngallery-dl --dump-json '%s' --range 0\n< gallery_path >)
UrlCheck2 --> UrlCheck3(检查是否是过时内容\n< gallery_path >/metadata/child.url是否存在)
UrlCheck3 --> UrlCheck4{child.url存在 ?}
UrlCheck4 -->|是| UrlCheck5(按照child.url更新URL为最新) --> UrlCheck1
UrlCheck4 -->|否| MetaCheck1[结束\n返回最新URL] --> OldPlacehold[后台执行\n过时元数据占位]
```

### 过时元数据占位

```mermaid
flowchart TD

UrlCheck1[输入URL] --> UrlCheck2(从URL中提取目标文件夹路径\ngallery-dl --dump-json '%s' --range 0\n< gallery_path >) --> MetaCheck1(检查元数据文件存在性\n< gallery_path >/metadata/*.json 文件存在)
MetaCheck1 --> MetaCheck2{元数据文件存在 ?}
MetaCheck2 -->|是| MetaCheck3(检查parent存在性\n元数据文件中存在parent字段) --> MetaCheck4{parent字段存在 ?} -->|是| UrlCheck3(按照parent字段更新URL为过时URL) --> UrlCheck1
UrlCheck3 --> OldPlacehold1(从URL中提取目标文件夹路径) --> OldPlacehold2[在目标文件夹路径下放置child.url]
MetaCheck2 -->|否| MetaCheck5(下载一个元数据\ngallery-dl -v '%s' --no-download --range 0)
MetaCheck4 -->|否| MetaCheck5 --> MetaCheck1
```

### 元数据下载

```mermaid
flowchart TD

UrlCheck1[输入URL] --> URL更新 --> UrlCheck2(从URL中提取目标文件夹路径\ngallery-dl --dump-json '%s' --range 0\n< gallery_path >) --> MetaCheck1(检查元数据文件存在性\n< gallery_path >/metadata/*.json 文件存在)
MetaCheck1 --> MetaCheck2{元数据文件存在 ?}
MetaCheck2 -->|是| MetaCheck4(检查元数据完整性\n< gallery_path >/metadata/*.json 每个文件都可json解析\n其中 'filecount' 值和 < gallery_path >/metadata/*.json 文件数相等)
MetaCheck4 --> MetaCheck5{元数据文件完整 ?}
MetaCheck5 -->|否| MetaCheck3
MetaCheck2 -->|否| MetaCheck3(下载元数据 gallery-dl -v '%s' --no-download) --> MetaCheck1
MetaCheck5 -->|是| MetaCheck6[结束]
MetaCheck3 --> MetaCheck6
```

### 图片下载

!!!!!!!!! TODO: 确定是最新之后，元数据下载和图片下载同时进行 !!!!!!!!!

```mermaid
flowchart TD
UrlCheck1[输入URL] --> UrlCheck2[URL更新] --> ImgCheck1(检查图片文件存在性: \n< gallery_path >/metadata/*.json 对应的每一个图片文件都存在) --> ImgCheck2{图片文件均存在 ?} -->|是| ImgCheck3(检查图片文件内容: \n< gallery_path >/metadata/*.json 对应的图片文件的SHA1值都与< image_token >字段值相符) --> ImgCheck4{图片文件内容均符合image_token ?} -->|是| ImgCheck5[结束]
ImgCheck2 -->|否| Download(调用gallery-dl下载)
ImgCheck4 -->|否| Download
Download --> ImgCheck5
```