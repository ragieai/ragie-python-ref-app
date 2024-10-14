import os
import time

from dotenv import load_dotenv
from ragie import Ragie

load_dotenv()

ragie = Ragie(
    auth=os.getenv('RAGIE_API_KEY'),
)

DOCUMENT_PARTITION = "test_partition"

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'examples', 'sample_podcast.txt')
    create_res = ragie.documents.create(request={
        "file": {
            "file_name": "sample_podcast.txt",
            "content": open(file_path, "rb"),
        },
        "metadata": {
            "scope": "tutorial"
        },
        # Partition is optional
        "partition": DOCUMENT_PARTITION
    })

    print(create_res)

    while True:
        res = ragie.documents.get(document_id=create_res.id)
        print(res.status)
        if res.status == "ready":
            break
        
        time.sleep(2)

    retrieval_res = ragie.retrievals.retrieve(request={
        "query": "What does Chamath think about Davos?",
        "filter_": {
            "scope": "tutorial"
        },
        "rerank": True,
        # Partition is optional
        "partition": DOCUMENT_PARTITION
    })

    print(retrieval_res)

if __name__ == "__main__":
    main()
