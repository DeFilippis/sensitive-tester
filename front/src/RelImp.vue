<template>
  <v-app class="main-app mt-3">
    <v-row align="center" justify="center">
      <v-card class="widecard p-3" >
        <v-card-actions class="d-flex justify-content-end" v-if="listFull">
          <v-btn color="error" @click="postit">
            {{ next }}
          </v-btn>
        </v-card-actions>
        <v-card-title>
          {{ title }}
        </v-card-title>
        <div>
          <div class="alert alert-danger" v-if="error">
            Move all the items based on the importance
          </div>
          <div class="row d-flex align-items-end ">
            <div class="col-6 ">{{ originalListTitle }}</div>
            <div class="col-6">{{ rankedListTitle }}</div>
          </div>
          <v-row class="d-flex  mx-1" align="center" justify="center">
            <RankList
              :itemslist="list1"
              @childlistchanged="listchanged"
            ></RankList>

            <RankList
              :itemslist="list2"
              :showRank="true"
              @childlistchanged="listchanged"
            ></RankList>

            <div v-for="(input, index) in list2" :key="index">
              <input :value="index" :name="input.label" type="hidden" />
            </div>
          </v-row>
        </div>
        <v-card-actions class="d-flex justify-content-end">
          <v-btn color="error" @click="postit" v-if="listFull">
            {{ next }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-app>
</template>

<script>
import _ from "lodash";
import RankList from "./RankList";
export default {
  components: { RankList },
  name: "Rank",
  data() {
    const { title, originalListTitle, rankedListTitle, next } = window.rank_obj;

    return {
      error: false,
      list1: _.clone(this.originalList),
      list2: [],
      title: title,
      next: next,
      originalListTitle: originalListTitle,
      rankedListTitle: rankedListTitle,

      options: {
        group: "people",
        ghostClass: "ghost",
      },
    };
  },
  computed: {
    listFull() {
      return this.list1.length === 0;
    },
  },
  methods: {
    listchanged() {
      this.error = false;
      // window.listFilled = this.list1.length === 0;
    },
    postit() {
      document.getElementById("form").submit();
    },
  },
};
</script>
<style>
[v-cloak] {
  display: none;
}
.main_card {
  max-width: 700px;
}

.item {
  border: 1px solid black;
}
.widecard {
  min-width: 550px;
}
</style>
