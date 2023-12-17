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
    <div v-if="response">
      <h2>Overall Word Cloud</h2>
      <vue-word-cloud :words="wordCloudData" style="height: 480px; width: 640px;">
      </vue-word-cloud>

      <h2>Positive Word Cloud</h2>
      <vue-word-cloud :words="posWordCloud" style="height: 480px; width: 640px;">
      </vue-word-cloud>

      <h2>Negative Word Cloud</h2>
      <vue-word-cloud :words="negWordCloud" style="height: 480px; width: 640px;">
      </vue-word-cloud>
  </div>
  </div>
</template>

<script>
import VueWordCloud from 'vuewordcloud';
import axios from 'axios'; // Import axios
export default {
  components: {
    [VueWordCloud.name]: VueWordCloud,
  },
  data() {
    return {
      videoUrl: "",
      response: null,
      wordCloudData: [],
      posWordCloud: [],
      negWordCloud: [],
    };
  },
  methods: {
    analyzeVideo() {
      // Send a POST request to your Flask backend
      axios({
        method: 'post', // Use POST request
        url: 'http://127.0.0.1:5000/analyze',
        data: {
          video_url: this.videoUrl,
        }
      }).then((response) => {
          this.response = response.data;
          this.wordCloudData = response.data.word_cloud_data;
          this.posWordCloud = response.data.pos_word_cloud;
          this.negWordCloud = response.data.neg_word_cloud;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      console.log('Analyze clicked')
      
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
