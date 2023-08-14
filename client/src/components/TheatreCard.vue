<template>
  <div class="card h-100">
    <div class="card-body">
      <router-link
        :to="'/view-theatre/' + theatre.id"
        class="card-title h5 text-decoration-none"
      >
        {{ theatre.name }}
      </router-link>
      <p class="card-text">{{ theatre.place }}</p>
      <p class="card-text">Capacity: {{ theatre.capacity }}</p>

      <!-- Display the first 3 shows of the theatre -->
      <div v-if="theatre.shows && theatre.shows.length" class="mt-3">
        <ul class="list-group">
          <li
            v-for="show in theatre.shows.slice(0, 3)"
            :key="show.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span>
              <strong>{{ show.name }}</strong
              ><br />
              {{ show.start_time }}
            </span>
            <span class="badge bg-secondary">₹{{ show.ticket_price }}</span>
          </li>
        </ul>
      </div>
      <!-- Show the 'More' button if there are more than 3 shows -->
      <button
        v-if="theatre.shows && theatre.shows.length > 3"
        class="btn btn-outline-secondary btn-sm"
        disabled
      >
        More
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "TheatreCard",
  props: {
    theatre: {
      type: Object,
      required: true,
    },
  },
};
</script>
