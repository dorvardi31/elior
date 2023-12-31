
import create_db_connection  # Assuming this is a module you have for DB connection



def find_sentence(sentence):
    sentence = sentence.lower().split()

    with create_db_connection.create_db_connection() as connection:
        cursor = connection.cursor()
        first_word = sentence[0]

        # Retrieve all occurrences of the first word
        cursor.execute("""
            SELECT concordance_row_num, concordance_word_num, log_file_id FROM combined_data_view 
            WHERE concordance_word = :word""",
            {'word': first_word})
        
        first_word_occurrences = cursor.fetchall()

        # Store the starting points of matched sequences
        matched_start_points = []

        # Verify the sequence for each occurrence of the first word
        for occ in first_word_occurrences:
            concordance_row_num, concordance_word_num, log_file_id = occ
            sequence_match = True

            for word_index, word in enumerate(sentence[1:], start=1):
                expected_word_num = concordance_word_num + word_index
                cursor.execute("""
                    SELECT COUNT(*) FROM combined_data_view 
                    WHERE concordance_word = :word 
                    AND concordance_row_num = :row_num 
                    AND concordance_word_num = :word_num 
                    AND log_file_id = :file_id""",
                    {'word': word, 'row_num': concordance_row_num, 'word_num': expected_word_num, 'file_id': log_file_id})

                if cursor.fetchone()[0] == 0:
                    sequence_match = False
                    break

            if sequence_match:
                matched_start_points.append((log_file_id, concordance_row_num, concordance_word_num))

        # Retrieve the full row with column names for each matched starting point
        detailed_matches = []
        for log_file_id, row_num, word_num in matched_start_points:
            cursor.execute("""
                SELECT * FROM combined_data_view 
                WHERE log_file_id = :file_id 
                AND concordance_row_num = :row_num 
                AND concordance_word_num = :word_num""",
                {'file_id': log_file_id, 'row_num': row_num, 'word_num': word_num})

            row_data = cursor.fetchone()
            if row_data:
                column_names = [desc[0] for desc in cursor.description]
                row_dict = dict(zip(column_names, row_data))
                detailed_matches.append(row_dict)

    return detailed_matches if detailed_matches else "No match found."
