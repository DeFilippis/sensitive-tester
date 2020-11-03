<template>
  <v-app>
    <v-container justify="center" align="center">
      <v-row justify="center" align="center">
        <v-col lg="6">
          <div>
            <v-card class="my-3">
              <v-card-title class="justify-center">
                <transition
                  name="custom-classes-transition"
                  enter-active-class="animate__animated animate__bounceIn"
                  
                >
                  <span
                    dark
                    :style="{ background: 'black' }"
                    class="white--text darken-2"
                    :key="body"
                    >{{ body }}</span
                  >
                </transition>
              </v-card-title>
              <div class="px-3 pb-3">
                Please drag the sliders below to divide it into three areas
                based on your estimate of how many people in this study have
                answered from 0 to 3, from 4 to 6, from 7 to 10 about the
                statement above.
              </div>
            </v-card>

            <div class="slider-wrapper">
              <div class="left-wrap"></div>

              <vue-slider
                @change="changingSliders"
                @drag-end="draggingEnd"
                class="slider-itself"
                :railStyle="rail"
                v-model="value"
                tooltip="none"
                :process="process"
                :min-range="0"
                :tooltip-placement="['bottom', 'top', 'top', 'bottom']"
                :dotOptions="[
                  { disabled: true, tooltip: 'none' },
                  { disabled: false, tooltip: 'none' },
                  { disabled: false, tooltip: 'none' },
                  { disabled: true, tooltip: 'none' },
                ]"
                :height="50"
                :enableCross="false"
              >
                <template v-slot:process="{ start, end, style, index }">
                  <div
                    :class="['vue-slider-process']"
                    :style="jopa(style, index)"
                  >
                    <div
                      class="merge-slider vue-slider-dot-tooltip-inner"
                      :class="inner(index, start, end)"
                    >
                      <span class="label">{{ get_label(index) }}</span>
                      <span class="percentage">
                        {{ (value[index + 1] - value[index]).toFixed(0) }}%
                      </span>
                    </div>
                  </div>
                </template>
                <template v-slot:dot="{ pos, index }">
                  <div :class="sliderStyle(pos, index)">
                    <v-icon dense class="shevron shevron-left" color="" v-if='!mergedSlider'>
                      mdi-chevron-left
                    </v-icon>
                    <v-icon dense class="shevron shevron-right">
                      mdi-chevron-right
                    </v-icon>
                  </div>
                </template>
              </vue-slider>
              <div class="right-wrap"></div>
            </div>
            <highcharts
              :options="chartOptions"
              :updateArgs="[true, true, true]"
            ></highcharts>
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <transition
            name="custom-classes-transition"
            enter-active-class="animate__animated animate__backInDown"
            leave-active-class="animate__animated animate__backOutDown"
          >
            <v-btn v-if="bothSlidersTouched" @click="deliver" color="error"
              >next</v-btn
            >
          </transition>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import VueSlider from "vue-slider-component";
import { Chart } from "highcharts-vue";
import "vue-slider-component/theme/default.css";
import _ from "lodash";
export default {
  components: {
    VueSlider,
    highcharts: Chart,
  },

  data: function() {
    return {
      body: "",
      mergedSlider:false,
      no_q_left: false,
      qid: null,
      distribution: {},
      slidersTouched: [false, false],
      bothSlidersTouched: false,
      initialValue: window.distribution,
      value: window.distribution,
      rail: {
        background: "gray",
        "border-radius": "0px",
      },
      process: (val) => [
        [val[0], val[1]],
        [val[1], val[2]],
        [val[2], val[3]],
      ],
      hcInstance: Chart,
      chartOptions: {
        chart: {
          height: 300,
          marginBottom: 20,
          type: "column",
          margin: [50, 50, 100, 80],
        },
        credits: { enabled: false },
        plotOptions: {
          column: {
            colorByPoint: true,
            borderRadius: 5,
          },
        },
        colors: ["black", "blue", "orange"],
        title: {
          text: "Distribution of answers",
        },
        xAxis: {
          categories: ["from 0 to 3", "from 4 to 6", "From 7 to 10"],
        },
        tooltip: {
          formatter: function() {
            return (
              "The value for <b>" +
              this.x +
              "</b> is <b>" +
              _.round(this.y) +
              "%</b> "
            );
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: "Share (in %)",
          },
        },
        legend: {
          enabled: false,
        },
        series: [
          {
            data: [33.3333333, 33.33333333, 33.33333333],
            dataLabels: {
              borderRadius: 5,
              backgroundColor: "rgba(252, 255, 197, 0.7)",
              borderWidth: 1,
              borderColor: "#AAA",
              enabled: true,
              x: 0,
              y: 35,
              format: "{y:.0f}%",
              style: {
                fontSize: "13px",
                fontFamily: "Verdana, sans-serif",
              },
            },
          },
        ],
      },
    };
  },
  mounted() {
    // console.debug(this.$options.sockets)
    this.$options.sockets.onmessage = (data) => {
      const d = JSON.parse(data["data"]);

      ({ body: this.body, id: this.qid, no_q_left: this.no_q_left } = d);
      this.value = _.clone(this.initialValue);
      this.slidersTouched = [false, false];
      this.bothSlidersTouched = false;
    };

    this.$options.sockets.onopen = (data) => {
      console.debug("pizda connected");
      this.$socket.sendObj({ info_request: true });
    };
  },
  watch: {
    no_q_left(val) {
      if (val) {
        document.getElementById("form").submit();
      }
    },
    value(newV, oldV) {
      var result = _.map(newV, function(e, i) {
        return newV[i + 1] - e;
      });

      result.pop();
      this.distribution = {
        first: result[0],
        second: result[1],
        third: result[2],
      };
      
      this.mergedSlider = _.includes(this.distribution,0);

      this.chartOptions.series[0].data = result;
    },
  },
  methods: {
    deliver() {
      console.debug("delivering");
      if (this.distribution && this.qid) {
        this.$socket.sendObj({
          qid: this.qid,
          distribution: this.distribution,
        });
      }
    },
    draggingEnd(index) {
      this.$socket.sendObj({ slider_movement_counter: true, qid: this.qid });
    },
    changingSliders(value, index) {
      this.slidersTouched[index - 1] = true;
      this.bothSlidersTouched = _.every(this.slidersTouched);
    },
    get_label(i) {
      const labs = ["from 0 to 3", "from 4 to 6", "from 7 to 10"];
      return labs[i];
    },
    x() {
      return this.value;
    },
    jopa(style, index) {
      const colors = ["black", "blue", "orange"];
      style["background"] = colors[index];

      if (index === 0) {
        return [style, "left-radius"];
      }
      return [style];
    },
    inner(index, s, e) {
      const classes = ["first", "second", "third"];

      if (this.value[index + 1] - this.value[index] < 5) {
        return "inv";
      }

      return classes[index];
    },
    sliderStyle(pos, index) {
      
      if (index===1 && this.mergedSlider) {
      console.debug('gonna invisible', index, this.mergedSlider)
        
        return 'inv'
        }
      if (index !== 0 && index !== 3) {
        return "slider-button";
      }
      return "inv";
    },
  },
};
</script>

<style>
:root {
  --animate-duration: 1800ms;
  --animate-delay: 2s;
}
.slide-fade-enter {
  transition: all 1s ease;
  transform: translateX(20px);
  opacity: 0;
}
.shevron {
  margin: -3px !important;
}
.left-wrap {
  background: black;
  border-radius: 10px 0px 0px 10px !important;
  width: 10px;
  margin: 7px 0px;
}
.right-wrap {
  background: orange;
  border-radius: 0px 10px 10px 0px !important;
  width: 10px;
  margin: 7px 0px 7px -1px;
  z-index: 4;
}
.slider-wrapper {
  display: flex;
  flex-direction: row;
}

.slider-itself {
  flex-grow: 1;
}

.vue-slider-process {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 0px 0px 0px 0px !important;
}
.left-radius {
  /* border-radius: 50px 0px 0px 50px !important; */
}
.right-radius {
  /* border-radius: 0px 50px 50px 0px !important; */
}
.jjj {
  width: 30px;
  background: yellow;
}
.inv {
  display: none;
}
.first {
  background: black !important;
}
.second {
  background: blue !important;
}
.third {
  background: orange !important;
}
.pizda {
  height: 100px !important;
}
.jopa {
  background: yellow !important;
  width: 100px !important;
  height: 100px;
}

.slider-button {
  width: 2em;
  height: 2em;
  background-color: white !important;
  position: absolute;
  border-radius: 2em;
  right: calc(-0.6em);
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  bottom: 0;
  margin: auto;
  z-index: 1010;
  cursor: ew-resize;
  user-select: none;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.merge-tooltip {
  position: absolute;
  left: 50%;
  bottom: 100%;
  transform: translate(-50%, -15px);
}
.label {
  color: white;
  font-weight: 700;
  user-select: none;
  display: block;
  overflow: hidden;
  font-family: sans-serif;
}
</style>
