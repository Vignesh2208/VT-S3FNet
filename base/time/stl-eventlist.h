/**
 * \file stl-eventlist.h
 * \brief Header file for S3F %event list, implemented using STL priority queue.
 */

#ifndef __STL_EVENTLIST_H__
#define __STL_EVENTLIST_H__

#ifndef __S3F_H__
#error "stl-eventlist.h can only be included by s3f.h"
#endif

/**
 * Compare two S3F events
 */
struct evt_Comparer
{
bool operator()(const EventPtr lhs, const EventPtr rhs) const
{
  if( lhs->__time > rhs->__time ) return true;
  if( lhs->__time < rhs->__time ) return false;
  if( lhs->__key2 > rhs->__key2)  return true;
  return false;
 }
};

/**
 * %Event list implementation using STL priority queue
 */
class STL_EventList : pq {
public:
	pthread_mutex_t  MUTEX;
	STL_EventList()
	{
		pthread_mutex_init(&MUTEX, NULL);
	}
	priority_queue<EventPtr, vector<EventPtr>, evt_Comparer> evtList;
	inline void push(EventPtr n)
	{
		pthread_mutex_lock(&MUTEX);
		evtList.push(n);
		pthread_mutex_unlock(&MUTEX);
	}
	inline void pop()
	{
		pthread_mutex_lock(&MUTEX);
		evtList.pop();
		pthread_mutex_unlock(&MUTEX);
	}
	inline bool empty()
	{
		pthread_mutex_lock(&MUTEX);
		bool isEmpty = evtList.empty();
		pthread_mutex_unlock(&MUTEX);
		return isEmpty;
	}
	inline int size()
	{
		pthread_mutex_lock(&MUTEX);
		int s = evtList.size();
		pthread_mutex_unlock(&MUTEX);
		return s;
	}
	EventPtr top()
	{
		pthread_mutex_lock(&MUTEX);
		EventPtr pppp = evtList.top();
		pthread_mutex_unlock(&MUTEX);
		return pppp;
	}

	inline bool empty_lockless()
	{
		bool isEmpty = evtList.empty();
		return isEmpty;
	}

	EventPtr top_lockless()
	{
		EventPtr pppp = evtList.top();
		return pppp;
	}

	inline void pop_lockless()
	{
		evtList.pop();
	}

	EventPtr nxt_relevant_netsim_event() {
		std::vector<EventPtr> tmpHolder;
		EventPtr relevant_netsim_event = NULL;

		if (evtList.empty())
			return relevant_netsim_event;
		pthread_mutex_lock(&MUTEX);
		while (evtList.size()) {
			relevant_netsim_event = evtList.top();
			evtList.pop();
			tmpHolder.push_back(relevant_netsim_event);

			if (relevant_netsim_event->get_evtype() != EVTYPE_MAKE_APPT &&
				relevant_netsim_event->get_evtype() != EVTYPE_CANCEL)
				break;
		} 
		for (auto it = tmpHolder.begin(); it != tmpHolder.end(); it++) {
			evtList.push(*it);
		}
		pthread_mutex_unlock(&MUTEX);	

		if (relevant_netsim_event->get_evtype() != EVTYPE_MAKE_APPT &&
			relevant_netsim_event->get_evtype() != EVTYPE_CANCEL)
			return relevant_netsim_event;
		return NULL;
	}
};
#endif /* __STL_EVENTLIST_H */

