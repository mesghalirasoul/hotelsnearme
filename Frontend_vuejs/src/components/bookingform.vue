<template>
<div id="app">
    <h2>Book This Property</h2>
    <h2>{{PropertyTitle}}</h2>
    <p>{{message}}</p>

    <form @submit.prevent=" createPost">
        <input placeholder="Customer Full Name" v-model="post.customer_name">
        <br>
        <input placeholder="Customer Phone Number" v-model="post.customer_phone_number">
        <br>
        <input placeholder="Customer Email" v-model="post.customer_email">
        <br>
        <DatepickerLite :name-attr="start_date.name" :value-attr="start_date.value" :year-minus="start_date.yearMinus" @value-changed="changeStartDate">
        </DatepickerLite>
        <DatepickerLite :name-attr="end_date.name" :value-attr="end_date.value" :year-minus="end_date.yearMinus" @value-changed="changeEndDate">
        </DatepickerLite>
        <br>
        <button type="submit">Submit</button> <button @click="cancelbooking">Cancel</button>
    </form>
</div>
</template>

<script>
import DatepickerLite from "vue3-datepicker-lite";
export default {
    name: "App",
    data() {
        return {
            message: "fill the below form",
            post: {
                property: {
                    title: "",
                    latitude: 11,
                    longitude: 20,
                    property_id: ""
                },
                customer_name: "",
                customer_phone_number: 999,
                customer_email: "",
                checkin_date: "",
                checkout_date: ""
            },
            data: {},
            start_date: {
                name: "Check In Date",
                value: "2020/10/01",
                yearMinus: "1911",
            },
            end_date: {
                name: "Check Out Date",
                value: "2020/10/02",
                yearMinus: "1911",
            },
            checkin_date: "",
            checkout_date: ""
        }
    },
    props: {
        PropertyTitle: String,
        PropertyId: String,
        PropertyLat: String,
        PropertyLng: String,
    },
    components: {
        DatepickerLite
    },

    methods: {
        onNavigate: function (e) {
            var view = e.sender.view();
            console.log(view.name); //the name of the current view
            var current = e.sender.current();
            console.log(current); //currently the focused date
        },
        cancelbooking() {
            this.$emit("nodisplay", false);
        },
        async createPost() {
            this.post.property.title = this.PropertyTitle
            this.post.property.latitude = this.PropertyLat
            this.post.property.longitude = this.PropertyLng
            this.post.property.property_id = this.PropertyId
            this.post.checkin_date = this.checkin_date.replace('/', '-').replace('/', '-');
            this.post.checkout_date = this.checkout_date.replace('/', '-').replace('/', '-');
            console.log(JSON.stringify(this.post))
            const request = new Request(
                    "/api/bookings", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    mode: "cors",
                    cache: "default",
                    body: JSON.stringify(this.post)
                }
            );
            fetch(request).then((response) => {
                    if (response.ok) {
                        this.message = "Data Successfully inserted!"
                        this.$emit("nodisplay", false);
                        return response.json();
                    } else {
                        throw new Error('Wrong Data! Try Again');
                    }
                })
                .then((responseJson) => {
                    // Do something with the response
                    console.log(responseJson)
                })
                .catch((error) => {
                    this.message = error
                    console.log(error)
                });
            // this.data = data;
            // console.log(response)

        },
        changeStartDate(value) {
            console.log(value + " selected!");
            this.checkin_date = value

        },
        changeEndDate(value) {
            console.log(value + " selected!");
            this.checkout_date = value
        }
    }
};
</script>

<style scoped>
#center {
    width: 480px;
    min-width: 480px;
    text-align: center;
    margin: 5% auto;
}
</style>
