<template>
  <v-app class='jopa' >
    <v-row align='center' justify='center' >

    
    <div v-cloak>
      <v-card flat class="py-12 main_card" v-if="!no_q_left && body">
        <v-card-text>
          <v-row align="center" justify="center">
            <v-col cols="12">
              <div v-if="q">{{ q }}</div>
            </v-col>
            <v-col cols="12">
              <div
                v-if="!no_q_left && body"
                class="lead purple darken-2 text-center"
              >
                <span class="white--text">{{ body }}</span>
              </div>
            </v-col>
            <v-col cols="12">
              <div v-if="no_q_left">No questions left</div>
            </v-col>

            <v-col cols="12">
              <v-btn-toggle v-model="value">
                <v-btn v-for="i in likert" :key="i" @click="answer(i)">
                  {{ i }}
                </v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>
    </v-row>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      type_correspondence: {
        attitude:
          'To what extent do you agree with the following statements (where "0" means "Totally disagree" and "10" means "Absolutely agree")',
        average_attitude:
          'How did the average participant of this study answer the question (where "0" means "Totally disagree" and "10" means "Absolutely agree")',
        friend:
          'Imagine two people who strongly disagree with each other on this question. (Person A answers "0", and Person B answers "10."). How likely is it that this disagreement would prevent them from being friends?',
      },
      no_q_left: false,
      body: null,
      qid: null,
      field: null,
      value: null,
      toggle_exclusive: undefined,
      likert: this._.range(0, 11),
    };
  },
  mounted() {
    // console.debug(this.$options.sockets)
    this.$options.sockets.onmessage = (data) => {
      const d = JSON.parse(data["data"]);
      ({
        no_q_left: this.no_q_left,
        body: this.body,
        id: this.qid,
        field: this.field,
        value: this.value,
      } = d);
    };
    this.$options.sockets.onopen = (data) => {
      console.debug("pizda connected");
      this.$socket.sendObj({ info_request: true });
    };
    //
  },
  computed: {
    q() {
      return this.type_correspondence[this.field];
    },
  },
  methods: {
    answer(val) {
      this.$socket.sendObj({
        answer: true,
        qid: this.qid,
        field: this.field,
        value: val,
      });
      this.value = null;
    },
  },
};
</script>
<style >
[v-cloak] {
  display: none;
}
.main_card {
  max-width: 700px;
}
#app{background:transparent}
 
</style>
