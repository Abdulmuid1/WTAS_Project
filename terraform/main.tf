# main.tf

provider "aws" {
  region = "ca-central-1"
}

# ECS Cluster
resource "aws_ecs_cluster" "wtas_cluster" {
  name = "wtas-cluster"
}

# IAM Role for ECS Task Execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# AWS managed policy for basic ECS tasks
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# CloudWatch Logs Full Access policy to the ECS task execution role
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_cloudwatch_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}


# ECS service 
resource "aws_ecs_service" "wtas_service" {
  name            = "wtas-service"
  cluster         = aws_ecs_cluster.wtas_cluster.id
  task_definition = aws_ecs_task_definition.wtas_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  
  # Allow ECS to restart the service and pick up the latest ECR image
  force_new_deployment = true

  # Make AWS wait longer before starting health checks
  health_check_grace_period_seconds = 120

  network_configuration {
    subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
    security_groups = [aws_security_group.wtas_ecs_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.wtas_target_group.arn
    container_name   = "wtas-container"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.wtas_listener]
}


# ECS Task Definition
resource "aws_ecs_task_definition" "wtas_task" {
  family                   = "wtas-task"  # Group name for the task 
  network_mode             = "awsvpc"  # Network required for Fargate
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "wtas-container",
    image     = "643989280406.dkr.ecr.ca-central-1.amazonaws.com/wtas-api:latest", # ECR image
    portMappings = [
      {
        containerPort = 8000
        protocol      = "tcp"
      },
    ],
    essential = true,
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        "awslogs-group"         = "/ecs/wtas-task",  # CloudWatch Logs Group
        "awslogs-region"        = "ca-central-1",       # Region
        "awslogs-stream-prefix" = "ecs"                  # Desired prefix
      }
    }
  }])
}

resource "aws_cloudwatch_log_group" "wtas_log_group" {
  name = "/ecs/wtas-task"  # Name of the log group for the ECS task
}


resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "wtas-vpc"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.5.0/24"  # Define the CIDR block for the subnet
  availability_zone       = "ca-central-1a"    # Specify the availability zone
  map_public_ip_on_launch = true

  tags = {
    Name = "wtas-public-subnet-a"
  }
}

# Create another subnet to handle high availability
resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.6.0/24"  # Define the CIDR block for the subnet
  availability_zone       = "ca-central-1b"    # Specify the availability zone
  map_public_ip_on_launch = true

  tags = {
    Name = "wtas-public-subnet-b"
  }
}



resource "aws_security_group" "wtas_lb_sg" {
  name        = "wtas-lb-sg"    # The security group name
  description = "Allow HTTP traffic from the internet to ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP inbound traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Public access
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "wtas_ecs_sg" {
  name        = "wtas-ecs-sg"    # The security group name
  description = "Allow HTTP from ALB to ECS tasks only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow traffic from Load balancer security group"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    security_groups = [aws_security_group.wtas_lb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "wtas_lb" {
  name               = "wtas-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups   = [aws_security_group.wtas_lb_sg.id]
  subnets            = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]  

  enable_deletion_protection = false
  enable_http2 = true
  idle_timeout             = 60
  tags = {
    Name = "wtas-lb"
  }
}

resource "aws_lb_target_group" "wtas_target_group" {
  name     = "wtas-target-group"
  port     = 8000      # The port the load balancer uses to forward requests to the container
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  target_type = "ip"      # awsvpc uses IP addresses

  health_check {
    path                = "/health"
    port                = "8000"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 5
    matcher             = "200-499"
  }
}

resource "aws_lb_listener" "wtas_listener" {
  load_balancer_arn = aws_lb.wtas_lb.arn
  port              = 80 # The port traffic uses to reach the load balancer
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.wtas_target_group.arn
  }
  depends_on = [aws_lb_target_group.wtas_target_group]

}

resource "aws_internet_gateway" "wtas_igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "wtas-igw"
  }
}

resource "aws_route_table" "wtas_route_table" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.wtas_igw.id
  }

  tags = {
    Name = "wtas-route-table"
  }
}

resource "aws_route_table_association" "wtas_route_table_association" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.wtas_route_table.id
}

resource "aws_route_table_association" "wtas_route_table_association_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.wtas_route_table.id
}

