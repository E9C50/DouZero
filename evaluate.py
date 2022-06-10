import os
import argparse

from douzero.evaluation.simulation import evaluate

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Dou Dizhu Evaluation')
    parser.add_argument('--landlord', type=str, default='baselines/douzero_WP/landlord.ckpt')
    parser.add_argument('--landlord_up', type=str, default='rlcard')
    parser.add_argument('--landlord_down', type=str, default='rlcard')
    parser.add_argument('--eval_data', type=str, default='eval_data.pkl')
    parser.add_argument('--num_workers', type=int, default=1)
    parser.add_argument('--gpu_device', type=str, default='')
    args = parser.parse_args()

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device

    evaluate(args.landlord,
             args.landlord_up,
             args.landlord_down,
             args.eval_data,
             args.num_workers)
