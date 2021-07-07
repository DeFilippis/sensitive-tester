<template>
  <div>
    <button v-on:click="increase">
      You clicked me {{ $store.state.count }} times.
    </button>
  </div>
</template>

<script>
export default {
  created() {
    console.debug('222',this.$store.state.count )
  },

  methods: {
    increase() {
      this.$store.commit("increment");
      
    },
  },
};
</script>
