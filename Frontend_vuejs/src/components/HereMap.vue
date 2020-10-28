<template>
<div id="map">
    <!--In the following div the HERE Map will render-->
    <div id="mapContainer" style="height:320px;width:480px" ref="hereMap"></div>
</div>
<div v-cloak>

    <div v-if="errorStr">
        Sorry, but the following error
        occurred: {{errorStr}}
    </div>

    <div v-if="gettingLocation">
        <i>Getting your location...</i>
    </div>

    <div v-if="location">
        Your location data is {{ location.coords.latitude }}, {{ location.coords.longitude}}
    </div>

</div>
<div>
    <p>Please Enter The latitude and longitude of your location</p>

    <p>
        Latitude is:
        <input v-model="user_lat" placeholder="">
    </p>
    <p>
        Longitude is:
        <input v-model="user_long" placeholder="">
    </p>

    <div id="example-2">
        <!-- `greet` is the name of a method defined below -->
        <button v-on:click="hotels">Find Hotels Near Me</button>
    </div>
</div>

<div id="center">
    <table>
        <tbody>
            <tr v-for="p in properties" v-bind:value="p.title" :key="p.title">
                <td style="float:left;">{{ p.title }}</td>
                <td><button @click="BookThisProperty(p)">Book</button></td>
            </tr>
        </tbody>
    </table>
</div>
<BookingForm v-if="show" :PropertyTitle="PropertyTitle" :PropertyId="PropertyId" :PropertyLat="PropertyLat" :PropertyLng="PropertyLng" @nodisplay="show=$event" />
</template>

<script>
import BookingForm from './bookingform'

export default {
    name: "HereMap",
    components: {
        BookingForm
    },
    props: {
        center: Object,
        latitude: String,
        longitude: String
    },
    data() {
        return {
            user_lat: '52.4',
            user_long: '13.4',
            platform: {},
            properties: {},
            apikey: "ugPraQLKoqBekVbHA1EJEfaQmVztnMYDhG-Q2tWUKTE",
            map: {},
            ui: {},
            location: null,
            gettingLocation: false,
            errorStr: null,
            yourlocation: {},
            show: false,
            ccenter: {
                lat: 52.5,
                lng: 13.4
            },
            PropertyTitle: "",
            PropertyId: "",
            PropertyLat: "",
            PropertyLng: "",
        };
    },
    mounted() {
        // Initialize the platform object:
        if (!("geolocation" in navigator)) {
            this.errorStr = 'Geolocation is not available.';
            return;
        }

        this.gettingLocation = true;
        // get position
        navigator.geolocation.getCurrentPosition(pos => {
            this.gettingLocation = false;
            this.location = pos;
        }, err => {
            this.gettingLocation = false;
            this.errorStr = err.message;
        })
        const platform = new window.H.service.Platform({
            apikey: this.apikey
        });
        this.platform = platform;
        this.initializeHereMap();
    },
    watch: {
        location: function (val) {
            console.log(val)
            this.ccenter.lat = this.location.coords.latitude
            this.ccenter.lat = this.location.coords.longitude
        },

    },
    methods: {
        BookThisProperty(value) {
            this.show = !this.show
            this.PropertyTitle = value.title
            this.PropertyId = value.property_id
            this.PropertyLat = value.latitude
            this.PropertyLng = value.longitude
            console.log(value.property_id)
        },
        initializeHereMap() { // rendering map

            const mapContainer = this.$refs.hereMap;
            const H = window.H;
            var maptypes = this.platform.createDefaultLayers();
            this.map = new H.Map(mapContainer, maptypes.vector.normal.map, {
                zoom: 10,
                center: this.center
            });
            addEventListener("resize", () => this.map.getViewPort().resize());
            // add behavior control
            new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));
            // add UI
            this.ui = H.ui.UI.createDefault(this.map, maptypes);
            // End rendering the initial map
        },

            
        hotels() {
            // console.log(process.env.VUE_APP_ROOT_API)
            let url = '/api/properties/?at=' + this.user_lat + ',' + this.user_long
            const H = window.H;
            var svgMarkup = '<svg width="24" height="24" ' +
                'xmlns="http://www.w3.org/2000/svg">' +
                '<rect stroke="white" fill="#1b468d" x="1" y="1" width="22" ' +
                'height="22" /><text x="12" y="18" font-size="12pt" ' +
                'font-family="Arial" font-weight="bold" text-anchor="middle" ' +
                'fill="white">H</text></svg>';

            console.log(this.location)
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // console.log(data);
                    this.properties = data
                    console.log(this.properties)
                    var icon = new H.map.Icon(svgMarkup);
                    data.forEach(place => {
                        console.log(place.latitude)
                        let marker = new H.map.Marker({
                            lat: place.latitude,
                            lng: place.longitude
                        });
                        marker.setData('<p>' + place.title + '</p>');
                        marker.addEventListener("tap", event => {
                            let bubble = new H.ui.InfoBubble(event.target.getGeometry(), {
                                content: event.target.getData()
                            });
                            this.ui.addBubble(bubble)
                            // });
                        }, {
                            icon: icon
                        });
                        this.map.addObject(marker);

                    });
                });
        }

    },

};
</script>

<style scoped>
#map {
    width: 480px;
    min-width: 480px;
    text-align: center;
    margin: 2% auto;
    background-color: #ccc;
}

#center {
    width: 480px;
    min-width: 480px;
    text-align: center;
    margin: 2% auto;
}
</style>
