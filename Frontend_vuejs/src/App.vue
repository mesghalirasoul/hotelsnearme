<template>
<div id="app">
    <HereMap :center="center" ref="map" latitude="37" longitude="-121" />
</div>
</template>

<script>
import HereMap from './components/HereMap'
export default {
    name: 'app',
    components: {
        HereMap
    },

    // mounted() {
    //     let map = this.$refs.map;
    //     map.hotels();

    // },
    data() {
        return {
            // we are this as prop to the HereMap component 
            center: {
                lat: 52.5,
                lng: 13.4
            }
        }

    }
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
