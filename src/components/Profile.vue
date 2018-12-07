<template>
  <div>
    <form @submit.prevent="changeDisplay">
      <div class="title-label">
        <label>{{display}}'s Profile</label>
      </div>
      <div class="form-group">
        <input type="text" placeholder="Enter New Display Name" class="form-control" v-model="newDisplay"></input>
      </div>
      <div class="bottom-row">
        <div class="update-button">
          <button type="submit" class="btn btn-default" style="float:left" v-on:click="changeDisplay()">Update Display Name</button>
        </div>
        <br>
        </br>
        <br>
        </br>
        <div class="deletion">
          <label>Would you like to delete your account? Click the button below to do so.</label>
          <br></br>
          <button type="submit" class="btn btn-default" style="float:left" v-on:click="deleteAccount()">Delete Account</button>
        </div>
        <button type="submit" class="btn btn-default" style="float:right" v-on:click="pushToHome()">Back</button>
      </div>
      <br></br>
    </form>
  </div>
</template>

<script>
  export default {
    data(){
      return {
        uName:'',
        id:'',
        display: '',
        newDisplay:'',
      }
    },
    beforeCreate: function(){
      document.body.className ='intro'
    },
    created : function() {
      this.getUser()
    },
    methods: {
      changeDisplay(){
        if(this.$cookies.get('user') == null || this.newDisplay.length < 1) {
          return
        }
        if(this.newDisplay.length < 1){
          alert("Display name is too short.")
        }
        this.$axios.put('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('user'),
          {"displayName": this.newDisplay})
        .then(response => {
          if(response.status == 200){

            console.log(this.id)
            this.getUser()
          }
        }).catch(error => {
          console.log(error)
        })
      },
      pushToHome(){
        this.$cookies.set('currentUserDisplayed', this.display)
        this.$router.push("/home")
      },
      deleteAccount(){
        this.$axios.delete('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('user'), { headers: {
          "Access-Control-Allow-Origin": '*'
        }})
        .then(response => {
          if(response.status == 204){
            this.$cookies.remove('user')
            this.$router.push("signup")
          }
        }).catch(error => {
          console.log(error)
        })
      },
      getUser(){
        this.$axios.get('https://info3103.cs.unb.ca:36479/users/'+ this.$cookies.get('user'))
        .then(response => {
          if(response.status == 200){
              this.uName = response.data.userInfo[0]["username"]
              this.id = response.data.userInfo[0]["listId"]
              this.display = response.data.userInfo[0]["displayName"]
          }
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }

</script>

<style scoped>

body{

}

.bottom-row {
  padding-bottom: 30px;
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

form button {
  border-radius: 20px;
  background-color: #D82E3B;
  border-color: ##D82E3B;
  color: white;
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


</style>
