CREATE TABLE IF NOT EXISTS output_tmp (document_name text,
        id int, 
        text text,
        document_id int,
        equation_id int,
        equation_text text,
        equation_offset text, 
        sentence_id int,
        sentence_offset int,
        sentence_text text,
        score float,
        sent_xpath text,
        sent_words text[],
        sent_top text[],
        sent_table_id int,
        sent_section_id int,
        sent_row_start int,
        sent_row_end int,
        sent_right int[],
        sent_position int,
        sent_pos_tags text[],
        sent_paragraph_id int,
        sent_page int[],
        sent_ner_tags text[],
        sent_name text,
        sent_lemmas text[],
        sent_left int[],
        sent_html_tag text,
        sent_html_attrs text[],
        sent_document_id int,
        sent_dep_parents text[],
        sent_dep_labels text[],
        sent_col_start int,
        sent_col_end int,
        sent_char_offsets int[],
        sent_cell_id int,
        sent_bottom int[],
        sent_abs_char_offsets int[],
        equation_variables text[],
        symbols text[],
        phrases text[],
        phrases_top text[],
        phrases_bottom text[],
        phrases_left text[],
        phrases_right text[],
        phrases_page text[],
        symbols_top int[],
        symbols_bottom int[],
        symbols_left int[],
        symbols_right int[],
        symbols_page int[],
        sentence_img text,
        equation_img text,
        UNIQUE (document_name, id)
        );

CREATE TABLE IF NOT EXISTS figures_tmp (
        target_img_path text,
        target_unicode text,
        target_tesseract text,
        assoc_img_path text,
        assoc_unicode text,
        assoc_tesseract text,
        html_file text,
        UNIQUE (target_img_path)
        );

CREATE TABLE IF NOT EXISTS tables_tmp (
        target_img_path text,
        target_unicode text,
        target_tesseract text,
        assoc_img_path text,
        assoc_unicode text,
        assoc_tesseract text,
        html_file text,
        UNIQUE (target_img_path)
        );
CREATE TABLE IF NOT EXISTS output (document_name text,
        id int, 
        text text,
        document_id int,
        equation_id int,
        equation_text text,
        equation_offset text, 
        sentence_id int,
        sentence_offset int,
        sentence_text text,
        score float,
        sent_xpath text,
        sent_words text[],
        sent_top text[],
        sent_table_id int,
        sent_section_id int,
        sent_row_start int,
        sent_row_end int,
        sent_right int[],
        sent_position int,
        sent_pos_tags text[],
        sent_paragraph_id int,
        sent_page int[],
        sent_ner_tags text[],
        sent_name text,
        sent_lemmas text[],
        sent_left int[],
        sent_html_tag text,
        sent_html_attrs text[],
        sent_document_id int,
        sent_dep_parents text[],
        sent_dep_labels text[],
        sent_col_start int,
        sent_col_end int,
        sent_char_offsets int[],
        sent_cell_id int,
        sent_bottom int[],
        sent_abs_char_offsets int[],
        equation_variables text[],
        symbols text[],
        phrases text[],
        phrases_top text[],
        phrases_bottom text[],
        phrases_left text[],
        phrases_right text[],
        phrases_page text[],
        symbols_top int[],
        symbols_bottom int[],
        symbols_left int[],
        symbols_right int[],
        symbols_page int[],
        sentence_img text,
        equation_img text,
        UNIQUE (document_name, id)
        );

CREATE TABLE IF NOT EXISTS figures (
        target_img_path text,
        target_unicode text,
        target_tesseract text,
        assoc_img_path text,
        assoc_unicode text,
        assoc_tesseract text,
        html_file text,
        UNIQUE (target_img_path)
        );

CREATE TABLE IF NOT EXISTS tables (
        target_img_path text,
        target_unicode text,
        target_tesseract text,
        assoc_img_path text,
        assoc_unicode text,
        assoc_tesseract text,
        html_file text,
        UNIQUE (target_img_path)
        );

CREATE VIEW figures_and_tables AS ( SELECT figures.target_img_path,
        figures.target_unicode,
        figures.target_tesseract,
        figures.assoc_img_path,
        figures.assoc_unicode,
        figures.assoc_tesseract,
        figures.html_file
        FROM figures
        UNION
        SELECT tables.target_img_path,
        tables.target_unicode,
        tables.target_tesseract,
        tables.assoc_img_path,
        tables.assoc_unicode,
        tables.assoc_tesseract,
        tables.html_file
        FROM tables);

CREATE VIEW docids AS ( SELECT DISTINCT "substring"(figures.target_img_path, '^(?:img/){1}(.*)?_input.*'::text) AS docid
   FROM figures);
