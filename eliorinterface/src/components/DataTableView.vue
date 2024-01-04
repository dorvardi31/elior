<template>
    <div class="container">
      <div class="file-upload-section">
        <file-upload @file-uploaded="fetchData"></file-upload>
      </div>
      
      <!-- Existing search section -->
      <div class="search-section">
        <input class="search-input" v-model="searchParams.CONCORDANCE_WORD" placeholder="Search by Concordance Word">
        <input class="search-input" v-model="searchParams.CONCORDANCE_ROW_NUM" placeholder="Search by Concordance Rownum">
        <input class="search-input" v-model="searchParams.CONCORDANCE_GROUPS" placeholder="Search by Concordance Group">
        <input class="search-input" v-model="searchParams.CONCORDANCE_WORD_NUM" placeholder="Search by Concordance Word Num">
        <input class="search-input" v-model="searchParams.ASSET_NAME" placeholder="Search by Asset Name">
        <input class="search-input" v-model="searchParams.ASSET_REGISTRATION_DATE" placeholder="Search by Asset Registration Date">
        <input class="search-input" v-model="searchParams.ASSET_TYPE" placeholder="Search by Asset Type">
        <input class="search-input" v-model="searchParams.EVENT_ID" placeholder="Search by Event ID">
        <input class="search-input" v-model="searchParams.EVENT_TYPE" placeholder="Search by Event Type">
        <input class="search-input" v-model="searchParams.EVIDENCE_REGEX" placeholder="Search by Evidence Regex">
        <input class="search-input" v-model="searchParams.FILE_NAME" placeholder="Search by File Name">
        <input class="search-input" v-model="searchParams.LOG_FILE_PATH" placeholder="Search by Log File Path">
        <input class="search-input" v-model="searchParams.IP_ADDR" placeholder="Search by IP Address">
        <input class="search-input" v-model="searchParams.USERNAME" placeholder="Search by Username">
        <input class="search-input" v-model="searchParams.USER_REGISTRATION_DATE" placeholder="Search by User Registration Date">
        <button class="search-button" @click="fetchData(true)">Search</button>
      </div>
      <div class="search-section">
        <input class="search-input" v-model="sentenceSearch" placeholder="Search by Sentence">
        <button class="search-button" @click="searchBySentence">Search Sentence</button>
      </div>
      <!-- Table with a button to view file content -->
      <div class="table-container">
        <table>
          <!-- Table Headings -->
          <thead>
            <tr>
              <th>Concordance Word</th>
              <th>Concordance Row Num</th>
              <th>Concordance Word Num</th>
              <th>Concordance Groups</th>
              <th>Asset Name</th>
              <th>IP Address</th>
              <th>Asset Type</th>
              <th>Asset Registration Date</th>
              <th>User Registration Date</th>
              <th>Username</th>
              <th>Event ID</th>
              <th>Event Type</th>
              <th>Log File ID</th>
              <th>File Name</th>
              <th>Log File Path</th>
              <th>View File</th>
            </tr>
          </thead>
          <!-- Table Body -->
          <tbody>
            <tr v-for="record in records" :key="record.id">
              <td>{{ record.CONCORDANCE_WORD }}</td>
              <td>{{ record.CONCORDANCE_ROW_NUM }}</td>
              <td>{{ record.CONCORDANCE_WORD_NUM }}</td>
              <td>{{ record.CONCORDANCE_GROUPS }}</td>
              <td>{{ record.ASSET_NAME }}</td>
              <td>{{ record.IP_ADDR }}</td>
              <td>{{ record.ASSET_TYPE }}</td>
              <td>{{ record.ASSET_REGISTRATION_DATE }}</td>
              <td>{{ record.USER_REGISTRATION_DATE }}</td>
              <td>{{ record.USERNAME }}</td>
              <td>{{ record.EVENT_ID }}</td>
              <td>{{ record.EVENT_TYPE }}</td>
              <td>{{ record.LOG_FILE_ID }}</td>
              <td>{{ record.FILE_NAME }}</td>
              <td>{{ record.LOG_FILE_PATH }}</td>
              <td><button @click="viewFileContent(record)">View Content</button></td>

            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Pagination -->
      <div class="pagination">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage <= 1">Previous</button>
        <span>Page {{ currentPage }}</span>
        <button @click="changePage(currentPage + 1)">Next</button>
      </div>
  
      <!-- Loading Indicator -->
      <div v-if="loading" class="loading">Loading...</div>
  
      <!-- Modal for File Content -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="showModal = false">&times;</span>
          <div v-html="selectedFileContent"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import FileUpload from './FileUpload.vue';
  
  export default {
    name: 'DataTableView',
    components: { FileUpload },
    data() {
      return {
        searchParams: {
          CONCORDANCE_WORD: '',
          CONCORDANCE_ROW_NUM: '',
          CONCORDANCE_WORD_NUM: '',
          CONCORDANCE_GROUPS: '',
          ASSET_NAME: '',
          ASSET_REGISTRATION_DATE: '',
          ASSET_TYPE: '',
          USER_REGISTRATION_DATE: '',
          USERNAME: '',
          EVENT_ID: '',
          EVENT_TYPE: '',
          LOG_FILE_ID: '',
          FILE_NAME: '',
          LOG_FILE_PATH: '',
          IP_ADDR: '',
            // ... other parameters
        },
  
        loading: false,
        records: [],
        currentPage: 1,
        selectedFileContent: '',
        showModal: false,
        sentenceSearch: '',
      };
    },
    methods: {
      fetchData(resetPage = false) {
        if (resetPage) {
          this.currentPage = 1;
        }
        this.loading = true;
        const params = {
          ...this.searchParams,
          page: this.currentPage,
          limit: this.pageSize
        };
        axios.get('http://127.0.0.1:5001/api/query_view', { params })
          .then(response => {
            this.records = response.data;
            this.loading = false;
          })
          .catch(error => {
            console.error('Error fetching data:', error);
            this.loading = false;
          });
      },
      searchBySentence() {
        this.loading = true;
        axios.post('http://127.0.0.1:5001/api/search', { query: this.sentenceSearch })
          .then(response => {
            this.records = response.data;  // Update the table with the new data
            this.loading = false;
          })
          .catch(error => {
            console.error('Error searching by sentence:', error);
            this.loading = false;
          });
      },
      changePage(newPage) {
        if (newPage > 0 && newPage !== this.currentPage) {
          this.currentPage = newPage;
          this.fetchData();
        }
      },
      viewFileContent(record) {
        this.showModal = true;
        this.selectedFileContent = '';

        const LOG_FILE_PATH = encodeURIComponent(record.LOG_FILE_PATH);
        const url = `http://127.0.0.1:5001/api/file_content?path=${LOG_FILE_PATH}&CONCORDANCE_WORD=${encodeURIComponent(record.CONCORDANCE_WORD)}&CONCORDANCE_ROW_NUM=${record.CONCORDANCE_ROW_NUM}&CONCORDANCE_WORD_NUM=${record.CONCORDANCE_WORD_NUM}`;

        console.log("Requesting URL:", url); // Log the URL for debugging

        axios.get(url)
        .then(response => {
            this.selectedFileContent = response.data.content;
        })
        .catch(error => {
            console.error('Error fetching file content:', error);
            this.selectedFileContent = 'Error loading content';
        });
    },

    },
    mounted() {
      this.fetchData();
    }
  };
  </script>
  
  <style>
    /* Base Container */
    .container {
      max-width: 1280px;
      margin: 2rem auto;
      padding: 2rem;
      font-family: 'Inter', sans-serif;
      background-color: #FAFAFA;
      color: #333;
    }

    /* File Upload Section */
    .file-upload-section {
      padding: 20px;
      margin-bottom: 30px;
      background: linear-gradient(145deg, #e6e6e6, #ffffff);
      border-radius: 12px;
      box-shadow: 12px 12px 24px #d6d6d6, -12px -12px 24px #ffffff;
    }

    /* Search Section */
    .search-section {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
      padding: 20px;
      border-radius: 12px;
      background: linear-gradient(145deg, #e6e6e6, #ffffff);
      box-shadow: 12px 12px 24px #d6d6d6, -12px -12px 24px #ffffff;
    }

    .search-input {
      padding: 15px;
      border: none;
      border-radius: 8px;
      box-shadow: inset 8px 8px 16px #d1d1d1, inset -8px -8px 16px #ffffff;
      transition: all 0.3s ease-in-out;
      font-size: 16px;
    }

    .search-input:focus {
      box-shadow: inset 4px 4px 8px #d1d1d1, inset -4px -4px 8px #ffffff;
    }

    .search-button {
      padding: 15px 30px;
      border: none;
      border-radius: 8px;
      background-color: #00BCD4; /* Cyan color */
      color: rgb(80, 131, 212);
      cursor: pointer;
      font-weight: 600;
      transition: background-color 0.3s;
      box-shadow: 4px 4px 8px #c4c4c4;
    }

    .search-button:hover {
      background-color: #00ACC1;
      box-shadow: 2px 2px 4px #c4c4c4;
    }

    /* Table Styles */
    .table-container {
      margin-top: 30px;
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    th, td {
      text-align: left;
      padding: 15px;
      border-bottom: 1px solid #ddd;
    }

    th {
      background-color: #00BCD4;
      color: white;
      font-weight: 600;
    }

    tr:nth-child(even) {
      background-color: #f2f2f2;
    }

    tr:hover {
      background-color: #e8f5e9;
    }

    /* Pagination Styles */
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 20px;
    }

    .pagination button {
      padding: 10px 20px;
      margin: 0 10px;
      border: none;
      border-radius: 8px;
      background-color: #00BCD4;
      color: white;
      cursor: pointer;
      transition: all 0.3s;
    }

    .pagination button:hover {
      background-color: #00ACC1;
    }

    .pagination span {
      font-weight: 600;
    }

    /* Loading Indicator */
    .loading {
      text-align: center;
      padding: 20px;
      font-size: 18px;
    }

    /* Modal Styles */
    .modal {
      display: block;
      position: fixed;
      z-index: 1000;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(5px);
    }

    .modal-content {
      background-color: #fff;
      margin: 10% auto;
      padding: 25px;
      border-radius: 12px;
      width: 50%;
      box-shadow: 12px 12px 24px #d6d6d6, -12px -12px 24px #ffffff;
    }

    .close {
      color: #aaa;
      float: right;
      font-size: 28px;
      font-weight: bold;
    }

    .close:hover,
    .close:focus {
      color: #000;
      text-decoration: none;
      cursor: pointer;
    }

  </style>
  