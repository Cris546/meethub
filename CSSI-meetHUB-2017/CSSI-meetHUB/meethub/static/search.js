function associate_events() {
  // $("#friend_response").hide();
  // $("#search_button_ok").click(show_friend_response);
}

$(document).ready(
   associate_events
);


// function show_friend_response(){
//   event.preventDefault();
//   var request_data = {
//     items: [],
//   }
//   items_list = $(".find_friend");
//   // var name = items_list.eq(i).children(".search_name").eq(0).val();
//   request_data.items.push({name: name});
//
//
//   $.post(
//   "/search",
//   JSON.stringify(request_data),
//   data_received
// )
// }

// function data_received(data){
//   console.log(data);
//   $("#possible_friends").text(data.name);
//   // $("#total").text(data.total);
//   $("#friend_response").show();
// }

// function practice(){
//   CssiUser
// }
