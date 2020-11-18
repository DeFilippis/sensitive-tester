<template>
    <div class="text-center">
        <v-dialog v-bind:value="dialog" v-on:input="emitOutput" width="500">
    
            <v-card>
                <v-card-title class="headline grey lighten-2">
                    Attention!
                </v-card-title>
    
                <v-card-text>
                    You commit some errors. Please pay more attention. Next time you fail to pass the attention test, we may finish the study
                </v-card-text>
    
                <v-divider></v-divider>
    
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="error" text @click="emitOutput">
                        Ok
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {
    props: {
        dialog: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        showDialog() {
            return this.dialog;
        }
    },
    methods: {
        emitOutput(value) {
      this.$emit('input', value)
    }
    }

}
</script>