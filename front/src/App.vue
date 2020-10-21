<template>
  <div>
    <div v-if="!no_q_left && body">{{ body }}</div>
    <div v-if="no_q_left">No questions left</div>
    <v-btn @click="jopa">JOPA</v-btn>
    <v-card flat class="py-12">
      <v-card-text>
        <v-row align="center" justify="center">
          <v-col cols="12">
            <v-btn-toggle v-model="toggle_exclusive" mandatory>
              <v-btn v-for='i in likert'>
                {{i}}
              </v-btn>
               
            </v-btn-toggle>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      no_q_left: false,
      body: null,
      qid: null,
      field: null,
      value: null,
      toggle_exclusive: undefined,
      likert: this._.range(0,11)
    };
  },
  mounted() {
    // console.debug(this.$options.sockets)
    this.$options.sockets.onmessage = (data) => {
      const d = JSON.parse(data["data"]);
      console.debug(
        "MESSAGE RECEIVCED",
        d
      )(
        ({
          no_q_left: this.no_q_left,
          body: this.body,
          id: this.qid,
          field: this.field,
          value: this.value,
        } = d)
      );
    };
    this.$options.sockets.onopen = (data) => {
      console.debug("pizda connected");
      this.$socket.sendObj({ info_request: true });
    };
    //
  },
  computed: {},
  methods: {
    jopa() {
      console.debug("JOPA CLICKED", this.body);
      this.$socket.sendObj({
        answer: true,
        qid: this.qid,
        field: this.field,
        value: Math.random(),
      });
    },
  },
};
</script>
<style scoped></style>
