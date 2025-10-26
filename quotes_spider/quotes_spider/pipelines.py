# quotes_spider/pipelines.py
import json

class CleanPipeline:
    def process_item(self, item, spider):
        # normalize text: strip quotes
        if item.get("text"):
            item["text"] = item["text"].strip().strip("“”\"")
        if "tags" in item and isinstance(item["tags"], list):
            item["tags"] = ",".join([t.strip() for t in item["tags"]])
        return item

class SaveJsonLinePipeline:
    def open_spider(self, spider):
        self.file = open("quotes.jl", "w", encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + "\n")
        return item

    def close_spider(self, spider):
        self.file.close()
