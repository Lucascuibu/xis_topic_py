import csv

def add_topic_to_csv(url):
    try:
        id_start_index = url.find('/topics/') + len('/topics/')
        id_end_index = url.find('?')
        curid = url[id_start_index:id_end_index]
        topic_name_start_index = url.rfind('/') + 1
        topic_name = url[topic_name_start_index:id_start_index -
                         len('/topics/')]
        with open('topic.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([topic_name, curid])
        print(f"Added topic {topic_name} to the CSV file.")
    except Exception as e:
        print(f"Error occurred while processing URL: {str(e)}")
