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

# AWS Managed Policies
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_cloudwatch_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

# Using a data source to reference an existing VPC instead of creating a new one
data "aws_vpc" "existing_vpc" {
  filter {
    name   = "tag:Name"
    values = ["existing-vpc-name"]  # Replace with the actual VPC name/tag
  }
}

# Using data sources for existing subnets
data "aws_subnet" "existing_subnet_a" {
  filter {
    name   = "tag:Name"
    values = ["existing-subnet-a"]
  }
}

data "aws_subnet" "existing_subnet_b" {
  filter {
    name   = "tag:Name"
    values = ["existing-subnet-b"]
  }
}

# Existing Internet Gateway
data "aws_internet_gateway" "existing_igw" {
  filter {
    name   = "tag:Name"
    values = ["existing-igw"]
  }
}

# ECS Service
resource "aws_ecs_service" "wtas_service" {
  name            = "wtas-service"
  cluster         = aws_ecs_cluster.wtas_cluster.id
  task_definition = aws_ecs_task_definition.wtas_task.arn
  desired_count   = 0
  launch_type     = "FARGATE"

  force_new_deployment = true
  health_check_grace_period_seconds = 60

  network_configuration {
    subnets          = [data.aws_subnet.existing_subnet_a.id, data.aws_subnet.existing_subnet_b.id]
    security_groups  = [aws_security_group.wtas_ecs_sg.id]
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
  family                   = "wtas-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "wtas-container",
    image     = "643989280406.dkr.ecr.ca-central-1.amazonaws.com/wtas-api:latest",
    portMappings = [
      {
        containerPort = 8000,
        protocol      = "tcp"
      }
    ],
    essential = true,
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        "awslogs-group"         = "/ecs/wtas-task",
        "awslogs-region"        = "ca-central-1",
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_cloudwatch_log_group" "wtas_log_group" {
  name = "/ecs/wtas-task"
}

resource "aws_security_group" "wtas_lb_sg" {
  name        = "wtas-lb-sg"
  description = "Allow HTTP traffic from the internet to ALB"
  vpc_id      = data.aws_vpc.existing_vpc.id  # Using existing VPC

  ingress {
    description = "Allow HTTP inbound traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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
  name        = "wtas-ecs-sg"
  description = "Allow HTTP from ALB to ECS tasks only"
  vpc_id      = data.aws_vpc.existing_vpc.id

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

data "aws_lb" "wtas_lb" {
  name = "wtas-lb"
}

resource "aws_lb_target_group" "wtas_target_group" {
  name     = "wtas-target-group"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = data.aws_lb.wtas_lb.vpc_id  # Ensure it matches existing LB's VPC
  target_type = "ip"

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
  load_balancer_arn = data.aws_lb.wtas_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.wtas_target_group.arn
  }

  depends_on = [aws_lb_target_group.wtas_target_group]
}

# Using the existing internet gateway
resource "aws_route_table" "wtas_route_table" {
  vpc_id = data.aws_vpc.existing_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = data.aws_internet_gateway.existing_igw.id
  }

  tags = {
    Name = "wtas-route-table"
  }
}

resource "aws_route_table_association" "wtas_route_table_association_a" {
  subnet_id      = data.aws_subnet.existing_subnet_a.id
  route_table_id = aws_route_table.wtas_route_table.id
}

resource "aws_route_table_association" "wtas_route_table_association_b" {
  subnet_id      = data.aws_subnet.existing_subnet_b.id
  route_table_id = aws_route_table.wtas_route_table.id
}