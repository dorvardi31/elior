import os
from flask_cors import CORS
from flask import Flask, jsonify, request
import cx_Oracle
import create_db_connection
import logging
import sys
import os
import search
from search import find_sentence
from datetime import datetime
app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Define the input directory where uploaded files will be saved
input_directory = '/opt/input'

api_endpoint = '/api/upload'

@app.route('/api/words', methods=['GET'])
def get_distinct_words():
    try:
        with create_db_connection.create_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT concordance_word FROM combined_data_view")
            words = [row[0] for row in cursor.fetchall()]
            return jsonify(words), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        search_sentence = data.get('query')  # Extracting the sentence from the request
        if not isinstance(search_sentence, str):
            return jsonify({'error': 'Invalid input type'}), 400

        # Process the search_sentence to find matches
        # Ensure any dictionary/set operations are using hashable types

        # Assuming find_sentence function returns a list of dictionaries
        results = find_sentence(search_sentence)
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/file_content', methods=['GET'])
def file_content():
    try:
        full_path = request.args.get('path')
        concordance_word = request.args.get('CONCORDANCE_WORD')
        row_num = int(request.args.get('CONCORDANCE_ROW_NUM')) - 1
        word_num = int(request.args.get('CONCORDANCE_WORD_NUM')) - 1

        if not full_path:
            return jsonify({'message': 'Full file path is required'}), 400

        if not os.path.exists(full_path):
            print("File not found at path:", full_path)  # Log the path for debugging
            return jsonify({'message': 'File not found at path: ' + full_path}), 404

        with open(full_path, 'r') as file:
            lines = file.readlines()

        start_line = max(0, row_num - 1)
        end_line = min(len(lines), row_num + 2)
        relevant_lines = lines[start_line:end_line]

        # Determine the target line index in the relevant_lines
        target_line_index = 0 if row_num == 0 else 1

        # Adjust word position for the extracted content
        words = relevant_lines[target_line_index].split()

        # If the word is on the first line of the file, no adjustment is needed
        if row_num == 0:
            word_num_adjusted = word_num
        else:
            word_num_adjusted = word_num - len(relevant_lines[0].split())

        # Highlight the specific word
        if 0 <= word_num_adjusted < len(words):
            words[word_num_adjusted] = f"<mark>{words[word_num_adjusted]}</mark>"
            relevant_lines[target_line_index] = " ".join(words)



        return jsonify({'content': "\n".join(relevant_lines)}), 200
    except Exception as e:
        print("An error occurred:", e)  # Log the exception for debugging
        return jsonify({'error': str(e)}), 500
    
@app.route(api_endpoint, methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']

        if not uploaded_file:
            return jsonify({'message': 'No file uploaded'}), 400

        # Save the uploaded file to the specified directory
        if not os.path.exists(input_directory):
            os.makedirs(input_directory)

        file_path = os.path.join(input_directory, uploaded_file.filename)
        uploaded_file.save(file_path)

        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

assign_groups_endpoint = '/api/assign_groups'

from flask import request


@app.route('/api/query_view', methods=['GET'])
def query_view():
    try:
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)
        start = (page - 1) * limit

        with create_db_connection.create_db_connection() as connection:
            cursor = connection.cursor()

            sql = "SELECT * FROM combined_data_view WHERE 1=1"
            params = {}

            for key, value in request.args.items():
                if key not in ['page', 'limit'] and value:  # Check if value is not empty
                    param_name = f"param_{key}"
                    sql += f" AND {key} = :{param_name}"
                    params[param_name] = value

            paginated_sql = f"""
                SELECT * FROM (
                    SELECT a.*, ROWNUM rnum FROM ({sql}) a
                ) WHERE rnum > :rownum_start AND rnum <= :rownum_end
            """
            params['rownum_start'] = start
            params['rownum_end'] = start + limit

            cursor.execute(paginated_sql, params)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify(result), 200
    except cx_Oracle.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception as general_error:
        return jsonify({'error': str(general_error)}), 500



@app.route('/api/assign_group', methods=['POST'])
def assign_groups():
    try:
        data = request.json
        words = data.get('words', [])  # List of words
        new_group = data.get('new_group', '')  # Group name

        if not words or not new_group:
            return jsonify({'message': 'Invalid input data'}), 400

        # Database connection
        with create_db_connection.create_db_connection() as connection:
            cursor = connection.cursor()
            try:
                for word in words:
                    # Assuming 'groups' is the column name where group names are stored
                    sql = "UPDATE concordance SET groups = :new_group WHERE word = :word"
                    cursor.execute(sql, {'new_group': new_group, 'word': word})
                connection.commit()
                return jsonify({'message': 'Groups assigned successfully'}), 200
            except Exception as e:
                connection.rollback()  # Rollback in case of error
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
