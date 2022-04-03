# def animate_map():
#     global data
#     date = start_time
#     num_days = (end_time-start_time).days+1
#     for _ in range(num_days):
#         # Increment day by 1
#         date += timedelta(days=1)
#         # Update data in map layers
#         seismic_layer.data = filter_date_range(data, start_time, end_time)
#         # Update the deck.gl map
#         map_deck.update()
#         # Render the map
#         map.pydeck_chart(map_deck)

#         # Update the maps and the subheading each day for 90 days
#         # Update the heading with current date
#         date_animation.subheader(f"Date:{date}")
#         # wait 0.1 second before go onto next day
#         time.sleep(0.5)
#     data = filter_date_range(data, start_time, end_time)


# st.button('Start Animation', on_click=animate_map)
