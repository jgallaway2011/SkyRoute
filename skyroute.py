from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

# Build your program below:
landmark_string = ''
for letter, landmark in landmark_choices.items():
  landmark_string += '{0} - {1}\n'.format(letter, landmark)

stations_under_construction = []

def skyroute():
  greet()
  user_type = get_user_type()
  if user_type == 'e':
    password = get_password()
    if password == 'verified':
      option = update_stations()
      if option == 'e':
        print('\nEmployee Logged Out!')
      else:
        back_to_employee_terminal()
    else:
      print('\nWe\'ll help you find the shortest route between the following Vancouver landmarks:\n' + landmark_string)
      new_route()
  elif user_type == 'c':
    print('\nWe\'ll help you find the shortest route between the following Vancouver landmarks:\n' + landmark_string)
    new_route()
  goodbye()

def back_to_employee_terminal():
  back_employee_option = input('\nWould you like to return to the employee terminal? Enter \'y\' for \'yes\' or \'n\' for \'no\': ')
  if back_employee_option == 'y':
    station_option = update_stations()
    if station_option == 'e':
      print('\nEmployee Logged Out!')
    else:
      back_to_employee_terminal()
  elif back_employee_option == 'n':
    print('\nEmployee Logged Out!')
  else:
        print('\nInvalid choice. Please try again!')
        back_to_employee_terminal()

def get_password():
  password = input('\nPlease enter password or \'c\' if a customer: ')
  if password.lower() == 'c':
    return 'c'
  elif password == 'password':
    return 'verified'
  else:
    print('\nInvalid Password. Please try again!')
    return get_password()

def update_stations():
  employee_action = input('\nWould you like to add or remove a station? Enter \'a\' for \'add\', \'r\' for \'remove\', \'s\' to run SkyRoute, or \'e\' for \'exit\': ').lower()
  if employee_action == 'a':
    station_to_add = input('\n What station would you like to add? ')
    stations_under_construction.append(station_to_add)
    print('\n{0} station was added to the list of stations under construction.'.format(station_to_add))
    return update_stations()
  elif employee_action == 'r':
    station_to_remove = input('\nWhat station would you like to remove? ')
    if station_to_remove in stations_under_construction:
      index = stations_under_construction.index(station_to_remove)
      stations_under_construction.pop(index)
      print('\n{0} station was removed from the list of stations under construction'.format(station_to_remove))
      return update_stations()
    else:
      print('\n{0} station was not in the list of stations under construction.'.format(station_to_remove))
      update_stations()
  elif employee_action == "s":
    print('\nWe\'ll help you find the shortest route between the following Vancouver landmarks:\n' + landmark_string)
    new_route()
  elif employee_action == 'e':
    return 'e'
  else:
    print('\nInvalid choice. Please try again!')
    return update_stations()

def greet():
  print('\nHi there and welcome to SkyRoute!')

def get_user_type():
  user_type = input('\nAre you a customer or employee? Enter \'c\' for \'customer\' or \'e\' for \'employee\': ').lower()
  if user_type == 'e' or 'c':
    return user_type
  else:
    print('\nInvalid choice. Please try again!')
    get_user_type()

def show_landmarks():
  see_landmarks = input('\nWould you like to see the list of landmarks again? Enter y/n: ').lower()
  if see_landmarks == 'y':
    print(landmark_string)
  elif see_landmarks == 'n':
    pass
  else:
    print('\nInvalid choice. Please try again!')
    show_landmarks()

def new_route(start_point = None, end_point = None):
  start_point, end_point = set_start_and_end(start_point, end_point)
  if start_point == end_point:
    print("\nPlease choose a destination different from origin. Otherwise, you're already here!")
  else:
    shortest_route = get_route(start_point, end_point)
    if shortest_route:
      shortest_route_string = '\n⬇️\n'.join(shortest_route)
      print('\nThe shortest metro route from {0} to {1} is:\n{2}'.format(start_point, end_point, shortest_route_string))
    else:
      print('\nUnfortunately, there is currently no path between {0} and {1} due to maintenance'.format(start_point, end_point))
  search_again(start_point, end_point)

def search_again(start_point, end_point):
  again = input('\nWould you like to see another route? Enter y/n: ').lower()
  if again == 'y':
    show_landmarks()
    new_route(start_point, end_point)
  elif again == 'n':
    pass
  else:
    print('\nInvalid choice. Please try again!')
    search_again(start_point, end_point)

def set_start_and_end(start_point, end_point):
  if start_point != None:
    change_point = input('\nWhat would you like to change?  You enter \'o\' for \'origin\', \'d\' for \'destination\', or \'b\' for \'both\': ').lower()
    if change_point == 'b':
      start_point = get_start()
      end_point = get_end()
    elif change_point == 'o':
      start_point = get_start()
    elif change_point == 'd':
      end_point = get_end()
    else:
      print('\nOpps, that isn\'t \'o\', \'d\', or \'b\'...')
      set_start_and_end(start_point, end_point)
  else:
    start_point = get_start()
    end_point = get_end()    
  return start_point, end_point

def get_route(start_point, end_point):
  start_stations = vc_landmarks[start_point]
  end_stations = vc_landmarks[end_point]
  routes = []
  for start_station in start_stations:
    for end_station in end_stations:
      metro_system = get_active_stations() if stations_under_construction else vc_metro
      if stations_under_construction:
        possible_route = dfs(metro_system, start_station, end_station)
        if not possible_route:
          return None
      route = bfs(metro_system, start_station, end_station)
      if route:
        routes.append(route)
  shortest_route = min(routes, key = len)
  return shortest_route

def get_start():
  start_point_letter = input("\nWhere are you coming from? Type in the corresponding letter: ").lower()
  if start_point_letter in landmark_choices.keys():
    start_point = landmark_choices[start_point_letter]
    return start_point
  else:
    print('\nSorry, that\'s not a landmark we have data on.  Let\'s try this again...')
    return get_start()

def get_end():
  end_point_letter = input("\nOk, where are you headed? Type in the corresponding letter: ").lower()
  if end_point_letter in landmark_choices.keys():
    end_point = landmark_choices[end_point_letter]
    return end_point
  else:
    print('\nSorry, that\'s not a landmark we have data on.  Let\'s try this again...')
    return get_end()

def get_active_stations():
  updated_metro = vc_metro
  for station_under_construction in stations_under_construction:
    for current_station, neighboring_stations in vc_metro.items():
      if current_station != station_under_construction:
        updated_metro[current_station] -= set(stations_under_construction)
      else:
        updated_metro[current_station] = set([])
  return updated_metro

def goodbye():
  print('\nThanks for using SkyRoute!')

skyroute()