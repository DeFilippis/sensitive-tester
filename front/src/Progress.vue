<template>
  <div class="fixed-top">
    <div class="progress progress2">
      <div
        class="progress-bar   "
        role="progressbar"
        :style="{ width: progressValue + '%' }"
        :aria-valuenow="progressValue"
        aria-valuemin="0"
        aria-valuemax="100"
      />
      <div
        class="justify-content-center d-flex position-absolute w-100 align-items-center align-self-center"
      >
        <div v-if='fixedProg'>{{ fixedProg }}%</div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
export default {
  props: ["progressValue"],
  data() {
    return {};
  },
  computed: {
    fixedProg() {
      return parseFloat(this.progressValue).toFixed(0);
    },
  },
};
</script>
<style></style>
