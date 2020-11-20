<template>
    <div class="text-center">
        <v-dialog v-bind:value="dialog" v-on:input="emitOutput" width="500">
    
            <v-card>
                <v-card-title class="headline grey lighten-2">
                    {{error.title}}
                </v-card-title>
    
                <v-card-text>
                    {{error.body}}
                </v-card-text>
    
                <v-divider></v-divider>
    
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="error" text @click="emitOutput">
                        {{error.button}}
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
        },
        error: {
            type: Object,
            default: ()=>{}
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