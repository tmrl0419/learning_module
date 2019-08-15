import src.model as sm
import src.api as sa

if __name__ =='__main__':
    token = sa.get_token('admin','devstack')
    model = sm.load_model('model/model')
    sm.predict( 10, 10, 10, 10, model)

