from aiohttp import web
import asyncio
from logging import info
        
class Handler:
    def __init__(self, loop, db):
        self.__loop = loop
        self.__db = db
        self.__customer_video_dict = {}
    
    async def watching(self, request):
        '''
        input:
        POST /watching
        BODY: {video_id: '<video identificator>', customer_id: '<customer identificator>'}
        output:
        Status 200
        '''
        data = await request.json()

        try:
            video_id, customer_id  = data['video_id'], data['customer_id']
            if customer_id in self.__customer_video_dict:
                if video_id in self.__customer_video_dict[customer_id]:
                    self.__customer_video_dict[customer_id][video_id].cancel()
            else:
                self.__customer_video_dict[customer_id]={}
    
            self.__customer_video_dict[customer_id][video_id] = self.__loop.create_task(self.process(customer_id, video_id))
                
            return web.Response()
        except BaseException as e:
            print('Error occured: {}'.format(e))
            return web.HTTPBadRequest()

    async def process(self, customer_id, video_id):
        '''
        This function responds for processing queries to /watching
        '''
        try :
            tr = self.__db.multi_exec()
            future1 = tr.hset('customer:{}'.format(customer_id), video_id, 1)
            future2 = tr.hset('video:{}'.format(video_id), customer_id, 1)
            result = await tr.execute()
            info('Created records for customer {} and video {}'.format(customer_id, video_id))

            await asyncio.sleep(5)
            
            tr = self.__db.multi_exec()
            future1 = tr.hdel('customer:{}'.format(customer_id), video_id)
            future2 = tr.hdel('video:{}'.format(video_id), customer_id)
            result = await tr.execute()
            info('Removed records for customer {} and video {}'.format(customer_id, video_id))

            if video_id in self.__customer_video_dict[customer_id]:
                self.__customer_video_dict[customer_id].pop(video_id)
        except asyncio.CancelledError:
            info('Task for customer {} with video {} canceled'.format(customer_id, video_id))

    async def customer_status(self, request):
        '''
        input:
        GET /customer/{customer_id}
        output:
        Status 200
        {watching: <number of streams customer {customer_id} watching now>}

        [WARN] if {customer_id} do not exist it returns {watching: 0}
        '''
        customer_id = request.match_info['customer_id']
        data = await self.__db.hgetall('customer:{}'.format(customer_id))
        return web.json_response({'watching': len(list(data.keys()))})

    async def video_status(self, request):
        '''
        input:
        GET /video/{video_id}
        output:
        Status 200
        {watching: <number of customers watching {video_id} stream now>}
        
        [WARN] if {video_id} do not exist it returns {watching: 0}
        '''
        video_id = request.match_info['video_id']
        data = await self.__db.hgetall('video:{}'.format(video_id))
        return web.json_response({'watching': len(list(data.keys()))})