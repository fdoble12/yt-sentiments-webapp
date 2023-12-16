<template>
  <div>
    <h1>YouTube Video Analysis</h1>
    <form @submit.prevent="analyzeVideo">
      <label for="video_url">Video URL:</label>
      <input type="text" id="video_url" v-model="videoUrl" required />
      <button type="submit">Analyze</button>
    </form>
    

    <div v-if="response">
      <h2>{{ response.video_title }}</h2>
      <h2>Analysis Result</h2>
      <p>Total Comments: {{ response.total_comments }}</p>
      <p>Total Positive Comments: {{ response.total_positive_comments }}</p>
      <p>Total Negative Comments: {{ response.total_negative_comments }}</p>
      <button @click="downloadCSV">Download CSV</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // Import axios
export default {
  data() {
    return {
      videoUrl: "",
      response: null,
    };
  },
  methods: {
    analyzeVideo() {
      // Send a POST request to your Flask backend
      console.log('Analyze clicked')
      axios
        .post("http://127.0.0.1:5000/analyze", {
          video_url: this.videoUrl,
        })
        .then((response) => {
          this.response = response.data;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    downloadCSV() {
      axios({
        method: 'post', // Use POST request
        url: 'http://127.0.0.1:5000/download-csv',
        data: {
          video_url: this.videoUrl,
        },
        responseType: 'blob', // Receive response as a blob (binary)
      })
        .then((response) => {
          // Create a Blob object and initiate the download
          const blob = new Blob([response.data], { type: 'text/csv' });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = 'classified_comments.csv';
          link.click();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  },
};
</script>

<style>
/* Add your CSS styling here */
</style>
