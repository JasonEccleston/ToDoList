<template>
  <div>
    <form @submit.prevent="signup">
      <div class="title-label">
        <label>Create Account</label>
      </div>
      <div class="form-group">
        <input type="text" placeholder="username" class="form-control" id="username" v-model="username">
      </div>
      <div class="form-group">
        <input type="text" placeholder="display name" class="form-control" id="displayname" v-model="displayName">
      </div>
      <div class="form-group">
        <input type="password" placeholder="password" class="form-control" id="password" v-model="password">
      </div>
      <div class="bottom-row">
        <div class="sign-up-link">
          <router-link to="/signin">
            <label style="float:left">Go back to login</label>
          </router-link>
        </div>
        <button type="submit" class="btn btn-default" style="float:right" v-on:click="signup()">Sign up</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data(){
    return {
      username: '',
      displayName: '',
      password: '',
      authenticated: false,
      status: '',
      output: {
        response: ''
      }
    }
  },
  beforeCreate: function() {
            document.body.className = 'intro';
  },
  methods: {
    signup(){
      this.$axios.post('https://info3103.cs.unb.ca:36479/signup',
      {'username': this.username, 'password': this.password, 'displayName': this.displayName, headers: {
        "Access-Control-Allow-Origin":'*'
      }})
      .then(response => {
        console.log(response.data);
        if(response.status==201){
          this.authenticated = true
          this.loggedin = response.data
          this.status = response.data.status
          this.$cookies.set('user', this.username)
          this.getUserId()
        }
      }).catch(error => {
        console.log(error)
        this.status = error.message;
      })
    },
    getUserId(){
      this.$axios.get('https://info3103.cs.unb.ca:36479/users/'+ this.username,{
        headers : {"Access-Control-Allow-Origin":'*'}
      }).
      then(response => {
        if(response.status == 200){
          console.log(response.data.userInfo[0]["listId"])
          this.$cookies.set('userId', response.data.userInfo[0]["listId"])
          this.$router.push("/home")
        }
      }).catch(error => {
        console.log(error)
        this.status = error.message
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.bottom-row {
  padding-bottom: 30px;
}

.sign-up-link {
  font-size: 8pt;
  align-self: 0 auto;
}


form {
  width: 30%;
  border-radius: 20px;
  background-color: #e6e6e6;
  padding: 20px;
  animation: bounce-in 0.5s;
  margin-top: 5%;
  margin-left: auto;
  margin-right: auto;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}

form button {
  border-radius: 20pt;
  background-color: #D82E3B;
  border-color: #D82E3B;
  color: white;
}

</style>
